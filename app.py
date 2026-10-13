import os
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from analyzer import extract_text, analyze_contract

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)

# In-memory demo history; use a database for multi-user/production deployment.
analyses = []

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html", analyses=analyses[:5], total=len(analyses))

@app.route("/analyze", methods=["POST"])
def analyze():
    if "contract" not in request.files:
        flash("Please choose a document to analyze.", "error")
        return redirect(url_for("index"))
    file = request.files["contract"]
    if not file or not file.filename:
        flash("Please choose a document first.", "error")
        return redirect(url_for("index"))
    if not allowed_file(file.filename):
        flash("Unsupported file type. Upload PDF, DOCX, or TXT.", "error")
        return redirect(url_for("index"))

    safe_name = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stored_path = UPLOAD_DIR / f"{timestamp}_{safe_name}"
    file.save(stored_path)
    try:
        text = extract_text(stored_path)
        if not text.strip():
            raise ValueError("No readable text was found. For scanned PDFs, run OCR first.")
        result = analyze_contract(text)
        result["filename"] = safe_name
        result["created_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
        result["word_count"] = len(text.split())
        result["preview"] = text[:1200]
        analyses.insert(0, result)
        analyses[:] = analyses[:20]
        return render_template("results.html", result=result)
    except Exception as exc:
        flash(f"Could not analyze this document: {exc}", "error")
        return redirect(url_for("index"))
    finally:
        try:
            stored_path.unlink(missing_ok=True)
        except OSError:
            pass

@app.route("/demo")
def demo():
    sample = """
    SERVICE AGREEMENT
    This agreement begins on January 1, 2026 and continues for twelve months.
    The client shall pay a fee of $2,500 per month within 15 days of invoice.
    Either party may terminate this agreement with 30 days written notice.
    The service provider may change prices at any time without prior notice.
    The client shall indemnify and hold harmless the provider from all claims.
    The provider's total liability shall not exceed one month's fees.
    All disputes shall be resolved through binding arbitration in a location selected by the provider.
    Confidential information must not be disclosed for five years after termination.
    """
    result = analyze_contract(sample)
    result.update({"filename": "sample_service_agreement.txt", "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                   "word_count": len(sample.split()), "preview": sample})
    analyses.insert(0, result)
    analyses[:] = analyses[:20]
    return render_template("results.html", result=result)

@app.route("/health")
def health():
    return {"status": "ok", "service": "ContractLens"}

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "true").lower() == "true")
