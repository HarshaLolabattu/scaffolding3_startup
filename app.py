"""
app.py – Final version for Parts 3 & 4
"""

from flask import Flask, request, jsonify, render_template
from starter_preprocess import TextPreprocessor
import traceback

app = Flask(__name__)
preprocessor = TextPreprocessor()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Text preprocessing service is running"
    })


@app.route('/api/clean', methods=['POST'])
def clean_text():
    """Clean text from a Project Gutenberg URL and return stats + summary"""
    try:
        data = request.get_json()
        url = data.get("url", "").strip()

        if not url or not url.endswith(".txt"):
            return jsonify({"success": False, "error": "Invalid or missing .txt URL"}), 400

        # Fetch, clean, normalize
        raw = preprocessor.fetch_from_url(url)
        clean = preprocessor.clean_gutenberg_text(raw)
        normalized = preprocessor.normalize_text(clean)

        # Compute stats and summary
        stats = preprocessor.get_text_statistics(normalized)
        summary = preprocessor.create_summary(normalized, num_sentences=3)

        return jsonify({
            "success": True,
            "cleaned_text": normalized,
            "statistics": stats,
            "summary": summary
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze raw pasted text and return statistics only"""
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"success": False, "error": "No text provided"}), 400

        normalized = preprocessor.normalize_text(text)
        stats = preprocessor.get_text_statistics(normalized)

        return jsonify({
            "success": True,
            "statistics": stats
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == '__main__':
    print("🚀 Starting Text Preprocessing Web Service...")
    print("📖 Available endpoints:")
    print("   GET  /           - Web interface")
    print("   GET  /health     - Health check")
    print("   POST /api/clean  - Clean text from URL")
    print("   POST /api/analyze - Analyze raw text")
    print()
    print("🌐 Open your browser to: http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')
