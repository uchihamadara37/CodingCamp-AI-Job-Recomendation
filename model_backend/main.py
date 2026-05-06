from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz  # pymupdf
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

app = FastAPI()

_stemmer = PorterStemmer()
_stop_words = set(stopwords.words("english"))

KNOWN_SKILLS = [
    "machine learning", "deep learning", "natural language processing", "computer vision",
    "data analysis", "data science", "data engineering", "data visualization",
    "software engineering", "software development", "web development", "mobile development",
    "cloud computing", "devops", "ci/cd", "version control", "agile", "scrum",
    "object oriented programming", "restful api", "rest api", "graphql",
    "microsoft office", "google analytics", "project management",
    "python", "java", "javascript", "typescript", "golang", "kotlin", "swift",
    "c++", "c#", "ruby", "php", "scala", "rust", "r",
    "react", "angular", "vue", "django", "flask", "fastapi", "spring", "laravel",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "node.js", "express", "next.js", "nuxt",
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite",
    "oracle", "sql server", "firebase", "dynamodb",
    "aws", "gcp", "azure", "docker", "kubernetes", "terraform", "ansible",
    "linux", "git", "jenkins", "github actions",
    "leadership", "communication", "teamwork", "problem solving", "critical thinking",
    "time management", "adaptability", "creativity",
]


def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


EXPERIENCE_SECTION_HEADERS = re.compile(
    r"(work experience|experience|employment|career|professional experience|work history|Pengalaman Kerja)",
    re.IGNORECASE,
)

EDUCATION_SECTION_HEADERS = re.compile(
    r"(education|academic|certification|training|course)",
    re.IGNORECASE,
)

DATE_RANGE_PATTERN = re.compile(
    r"((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[\s,]*\d{4}|\d{4})"
    r"\s*[-–—to]+\s*"
    r"((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[\s,]*\d{4}|\d{4}|present|current|now)",
    re.IGNORECASE,
)


def extract_experience(text: str) -> list[dict]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    exp_start = None
    exp_end = len(lines)
    for i, line in enumerate(lines):
        if EXPERIENCE_SECTION_HEADERS.search(line) and exp_start is None:
            exp_start = i + 1
        elif exp_start is not None and EDUCATION_SECTION_HEADERS.search(line):
            exp_end = i
            break

    if exp_start is None:
        return []

    exp_lines = lines[exp_start:exp_end]

    experiences = []
    current: dict = {}
    desc_buffer: list[str] = []

    def flush():
        if current:
            current["description"] = " ".join(desc_buffer).strip()
            experiences.append({**current})
            current.clear()
            desc_buffer.clear()

    for line in exp_lines:
        date_match = DATE_RANGE_PATTERN.search(line)
        if date_match:
            flush()
            current["duration"] = date_match.group(0).strip()
            title_part = line[: date_match.start()].strip(" |-–—")
            if title_part:
                current["title"] = title_part
        elif current:
            if "title" not in current and "company" not in current:
                current["title"] = line
            elif "company" not in current:
                current["company"] = line
            else:
                desc_buffer.append(line)

    flush()
    return experiences


def extract_skills(text: str) -> list[str]:
    text_lower = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    return found


def preprocess_text(text: str) -> str:
    """
    Preprocessing pipeline for TF-IDF + cosine similarity:
    1. Lowercase
    2. Remove special characters and digits
    3. Tokenize
    4. Remove stopwords
    5. Stem
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in _stop_words and len(t) > 2]
    tokens = [_stemmer.stem(t) for t in tokens]
    return " ".join(tokens)


@app.post("/extract-cv")
async def extract_cv(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf",):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    raw_text = extract_text_from_pdf(file_bytes)

    if not raw_text:
        raise HTTPException(status_code=422, detail="Could not extract text from the PDF")

    preprocessed_text = preprocess_text(raw_text)
    skills = extract_skills(raw_text)
    experience = extract_experience(raw_text)

    return {
        "filename": file.filename,
        "preprocessed_text": preprocessed_text,
        "skills": skills,
        "experience": experience,
    }


def main():
    print("Hello from model-backend!")


if __name__ == "__main__":
    main()
