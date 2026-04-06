# TommysTool
Converts CSV to Canvas QTI Zip file. 

# Tommy’s Tool 🎓

A simple desktop utility for converting CSV-based question banks into **Canvas-compatible QTI zip files**.

Built to streamline the workflow for professors and educators generating quiz content with ChatGPT or spreadsheets.

---

## 🚀 Features

* ✅ Convert CSV question banks into Canvas QTI format
* ✅ Paste CSV directly (no file saving required)
* ✅ Supports multiple CSV formats:

  * `Option A / Option B / Option C / Option D`
  * OR `A / B / C / D`
* ✅ Right-click support (cut / copy / paste)
* ✅ Automatic input clearing after conversion
* ✅ Simple GUI (no command line required)

---

## 📦 Example Input Formats

### Standard Format

```
Question,Option A,Option B,Option C,Option D,Correct Answer
"What is 2+2?","1","2","3","4","D"
```

### ChatGPT-Friendly Format

```
Question,A,B,C,D,Answer
"What is 2+2?","1","2","3","4","D"
```

---

## 🛠️ Installation

### Requirements

* Python 3.8+

### Steps

1. Clone the repository:

```
git clone https://github.com/yourusername/tommys-tool.git
cd tommys-tool
```

2. Run the application:

```
python main.py
```

---

## 🖥️ Usage

### Option 1: Paste CSV (Fastest)

1. Copy CSV output (e.g., from ChatGPT)
2. Paste into the text box (right-click works)
3. Click **Convert to QTI Zip**
4. Save your `.zip` file
5. Upload to Canvas

---

### Option 2: Load Existing CSV

1. Click **Browse**
2. Select a `.csv` file
3. Click **Convert to QTI Zip**
4. Save and upload to Canvas

---

## 📤 Importing into Canvas

1. Go to your course in Canvas
2. Navigate to **Settings → Import Course Content**
3. Select:

   * **Content Type:** QTI `.zip file`
4. Upload the generated zip file
5. Import questions into your question bank

---

## ⚠️ Common Issues

### ❌ “Missing required data” error

* Ensure your CSV includes:

  * Question
  * Four answer choices (A–D)
  * Correct answer (A, B, C, or D)

---

### ❌ Formatting Issues from ChatGPT

* Make sure output is:

  * Proper CSV
  * Fields wrapped in quotes
  * No extra text before/after

---

## 🧠 Why This Exists

Many educators use ChatGPT to generate quiz content, but converting that into Canvas-compatible formats is tedious.

**Tommy’s Tool eliminates the manual steps**:

```
Before:
ChatGPT → copy → save → rename → import → fix errors 😩

After:
ChatGPT → paste → click → done ✅
```

---

## 🛣️ Roadmap

* [ ] JSON input support
* [ ] Question preview table
* [ ] Multi-answer / true-false support
* [ ] Direct ChatGPT API integration
* [ ] Canvas API upload

---

## 🤝 Contributing

Pull requests are welcome!
If you have ideas to improve usability for educators, feel free to open an issue.

---

## 📄 License

MIT License

---

## 👨‍🏫 Acknowledgments

Named after **Tommy**, a professor who inspired this tool by needing a faster way to build question banks.

---

## ⭐ If This Helped You

Give the repo a star—it helps others find it!
