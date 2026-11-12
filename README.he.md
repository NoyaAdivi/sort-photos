<div dir="rtl">

<p align="center">
  <a href="https://github.com/NoyaAdivi/sort-photos"><img src="docs/readme/banner-he.svg" width="100%" alt="Sort Photos: מסווג תמונות AI שעובד בלי אינטרנט"></a>
</p>

<p align="center"><a href="README.md"><img src="docs/readme/lang-en.svg" height="44" alt="Read in English"></a></p>

<p align="center">
  <a href="#quick-start"><img src="https://img.shields.io/badge/%D7%94%D7%AA%D7%97%D7%9C%D7%94_%D7%9E%D7%94%D7%99%D7%A8%D7%94-FFD5C9?style=for-the-badge&logo=rocket&logoColor=A8483A" alt="התחלה מהירה"></a>
  <a href="#how-it-works"><img src="https://img.shields.io/badge/%D7%90%D7%99%D7%9A_%D7%96%D7%94_%D7%A2%D7%95%D7%91%D7%93-DAD5FF?style=for-the-badge&logo=pytorch&logoColor=5548C8" alt="איך זה עובד"></a>
  <a href="sort_photos.py"><img src="https://img.shields.io/badge/%D7%9C%D7%A7%D7%95%D7%93-D9F3E7?style=for-the-badge&logo=python&logoColor=1F7350" alt="לקוד"></a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/NoyaAdivi/sort-photos?color=DAD5FF&labelColor=5548C8" alt="License"></a>
  <a href="https://github.com/NoyaAdivi/sort-photos/commits/main"><img src="https://img.shields.io/github/last-commit/NoyaAdivi/sort-photos?color=FFD5C9&labelColor=A8483A" alt="Last commit"></a>
  <a href="https://github.com/NoyaAdivi/sort-photos"><img src="https://img.shields.io/github/languages/top/NoyaAdivi/sort-photos?color=D9F3E7&labelColor=1F7350" alt="Top language"></a>
  <a href="https://github.com/NoyaAdivi/sort-photos"><img src="https://img.shields.io/github/repo-size/NoyaAdivi/sort-photos?color=FBD5E0&labelColor=A03A5C" alt="Repo size"></a>
</p>

<h3 align="center">מפרידים בין המסמכים לזכרונות, בלי לתייג אף תמונה.</h3>

<p align="center">
  Sort Photos עובר על אוסף תמונות גדול ומחלק אותו ל<b>מסמכים</b> (קבלות, דפים, צילומי מסך, פתקים, תעודות)<br>ול<b>תמונות</b> (אנשים, משפחה, מקומות, אוכל) בעזרת מודל <a href="https://github.com/mlfoundations/open_clip">CLIP</a> שלא צריך אימון.
</p>

<table align="center">
  <tr>
    <td align="center" width="25%"><a href="#how-it-works"><b>🧠 0</b></a><br><sub>תיוגים או אימון</sub></td>
    <td align="center" width="25%"><a href="#highlights"><b>🔒 100%</b></a><br><sub>בלי אינטרנט, פרטי</sub></td>
    <td align="center" width="25%"><a href="#output"><b>📁 3</b></a><br><sub>תיקיות פלט</sub></td>
    <td align="center" width="25%"><a href="#formats"><b>🖼️ 7</b></a><br><sub>פורמטים של תמונות</sub></td>
  </tr>
</table>

<a name="highlights"></a>
<p align="center"><a href="#highlights"><img src="docs/readme/highlights-he.svg" width="100%" alt="מה מיוחד בו"></a></p>

<table>
  <tr valign="top">
    <td width="33%"><p><b>🧠 חכם בלי אימון</b></p><ul><li><b>Zero-shot:</b> כל תמונה מושווית לתיאורים קצרים בטקסט</li><li><b>סף ביטחון:</b> תמונות שהמודל לא בטוח בהן עוברות ל־<code>uncertain/</code></li><li><b>קל להרחבה:</b> מוסיפים תיאור או תיקייה חדשה שלמה</li></ul></td>
    <td width="33%"><p><b>🔒 בטוח לתמונות שלך</b></p><ul><li><b>עובד בלי אינטרנט</b> אחרי ההורדה הראשונה של המודל</li><li><b>מעתיק ולא מזיז</b> כברירת מחדל, התיקייה המקורית לא משתנה</li><li><b>אפשר להמשיך:</b> עוצרים עם Ctrl+C ומריצים שוב</li></ul></td>
    <td width="33%"><p><b>⚡ מהיר גם במחשב ישן</b></p><ul><li><b>קוונטיזציה ל־int8</b> לפי 1.5 עד 2 מהירות במעבד</li><li><b>פענוח JPEG מהיר</b> וטעינה במקביל</li><li><b>הרצת ניסיון</b> על מדגם כדי לבדוק תוצאות ומהירות</li></ul></td>
  </tr>
</table>

<a name="how-it-works"></a>
<p align="center"><a href="#how-it-works"><img src="docs/readme/how-it-works-he.svg" width="100%" alt="איך זה עובד"></a></p>

```mermaid
flowchart RL
  A(["📂 תיקיית התמונות"]) --> B["טעינה והקטנה<br/>במקביל"]
  B --> C["CLIP ViT-B-32<br/>ייצוג של התמונה"]
  P(["תיאורים בטקסט<br/>'a photo of a receipt'<br/>'a family photo'"]) --> C
  C --> D{"ביטחון<br/>0.75 ומעלה?"}
  D -->|כן| E(["📄 documents/"])
  D -->|כן| F(["🖼️ photos/"])
  D -->|לא| G(["🤔 uncertain/"])
  C --> R(["📊 results.csv"])
  style A fill:#E8E4FF,stroke:#6F60F0,color:#2C2668
  style P fill:#FFE6DE,stroke:#E36E57,color:#2C2668
  style E fill:#D9F3E7,stroke:#1F7350,color:#1F4D38
  style F fill:#D9F3E7,stroke:#1F7350,color:#1F4D38
  style G fill:#FFF1C9,stroke:#B98A1E,color:#5C4410
  style R fill:#DAD5FF,stroke:#5548C8,color:#2C2668
```

כל תמונה מקבלת ציון מול שתי קבוצות של תיאורים בטקסט, והקבוצה עם ההסתברות הכוללת הגבוהה ביותר מנצחת. מתחת לסף (0.75 כברירת מחדל) התמונה עוברת ל־<code>uncertain/</code> לבדיקה מהירה ביד.

<a name="output"></a>
<details open>
<summary><b>📁 מה מקבלים בסוף</b></summary>

```
Sorted/
├── documents/    מבנה תתי התיקיות המקורי נשמר
├── photos/
├── uncertain/    תמונות עם ביטחון נמוך, כדאי לעבור עליהן ביד
└── results.csv   שורה לכל תמונה: קטגוריה, ביטחון, ציונים, נתיב היעד
```
קבצים פגומים או כאלה שלא נפתחים נרשמים כ־<code>error</code> ב־<code>results.csv</code> ולא מועתקים.
</details>

<a name="tech-stack"></a>
<p align="center"><a href="#tech-stack"><img src="docs/readme/tech-stack-he.svg" width="100%" alt="טכנולוגיות"></a></p>

<p align="center">
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-CFE6FA?style=for-the-badge&logo=python&logoColor=3F6D9F" alt="Python"></a>
  <a href="https://pytorch.org"><img src="https://img.shields.io/badge/PyTorch-FBD5E0?style=for-the-badge&logo=pytorch&logoColor=A03A5C" alt="PyTorch"></a>
  <a href="https://github.com/mlfoundations/open_clip"><img src="https://img.shields.io/badge/OpenCLIP-DAD5FF?style=for-the-badge&logo=openai&logoColor=5548C8" alt="OpenCLIP"></a>
  <a href="https://python-pillow.org"><img src="https://img.shields.io/badge/Pillow-D9F3E7?style=for-the-badge&logo=python&logoColor=1F7350" alt="Pillow"></a>
  <a href="https://pandas.pydata.org"><img src="https://img.shields.io/badge/pandas-FFD5C9?style=for-the-badge&logo=pandas&logoColor=A8483A" alt="pandas"></a>
</p>

<a name="quick-start"></a>
<p align="center"><a href="#quick-start"><img src="docs/readme/quick-start-he.svg" width="100%" alt="התחלה מהירה"></a></p>

צריך **Python 3.9 ומעלה**. הקובץ [`requirements.txt`](requirements.txt) מתקין את הגרסה הקטנה של PyTorch למעבד בלבד. עם כרטיס NVIDIA, מתקינים קודם את PyTorch מ־[pytorch.org](https://pytorch.org/get-started/locally/).

```bash
pip install -r requirements.txt
```

1. **הרצת ניסיון על 300 תמונות** (מסווג וכותב `results.csv`, לא מעתיק כלום):
   ```bash
   python sort_photos.py "D:\Pictures" "D:\Sorted" --dry-run --limit 300
   ```
2. **בודקים** את `D:\Sorted\results.csv` ואז מוחקים אותו.
3. **ממיינים הכול:**
   ```bash
   python sort_photos.py "D:\Pictures" "D:\Sorted"
   ```

> [!NOTE]
> תיקיית הפלט לא יכולה להיות בתוך תיקיית המקור. בהרצה הראשונה המודל יורד (בערך 600 MB).

<details>
<summary><b>⚙️ כל האפשרויות</b></summary>

| אפשרות | מה היא עושה |
| --- | --- |
| `--dry-run` | רק מסווג וכותב `results.csv`, בלי להעתיק או להזיז |
| `--limit N` | מטפל רק ב־N התמונות החדשות הראשונות |
| `--threshold X` | ביטחון מינימלי להחלטה (ברירת מחדל `0.75`) |
| `--move` | מזיז קבצים במקום להעתיק |
| `--batch-size N` | תמונות בכל קבוצה (ברירת מחדל `32`), להוריד אם נגמר הזיכרון |
| `--no-quantize` | מבטל את ההאצה של int8 |
| `--workers N` | תהליכונים לטעינת תמונות (ברירת מחדל: מספר הליבות) |
| `--threads N` | תהליכונים של PyTorch (ברירת מחדל: כל הליבות) |
</details>

<details>
<summary><b>🎯 איך לשפר את הדיוק</b></summary>

עורכים את המילון `CATEGORIES` בראש הקובץ [`sort_photos.py`](sort_photos.py). אם סוג מסוים של תמונה ממשיך להגיע למקום הלא נכון, מוסיפים לקבוצה הנכונה תיאור שמתאר אותו, למשל `"a photo of a medical prescription"` תחת `documents`. קבוצה חדשה, כמו `"screenshots"`, מקבלת תיקיית פלט משלה אוטומטית.
</details>

<a name="formats"></a>
<details>
<summary><b>🖼️ פורמטים ומהירות</b></summary>

JPG, PNG, BMP, WEBP, TIFF, GIF ו־HEIC/HEIF (דרך `pillow-heif`). במחשב נייד ישן עם 2 עד 4 ליבות, 40,000 תמונות לוקחות בערך 30 עד 90 דקות. סרגל ההתקדמות מראה כמה תמונות בשנייה.
</details>

<a name="contact"></a>
<p align="center"><a href="#contact"><img src="docs/readme/footer-he.svg" width="100%" alt="נבנה על ידי נויה אדיבי"></a></p>

<p align="center">
  <a href="https://github.com/NoyaAdivi/sort-photos"><img src="https://img.shields.io/badge/%D7%9C%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98-FFD5C9?style=for-the-badge&logo=github&logoColor=A8483A" alt="לפרויקט"></a>
  <a href="https://www.linkedin.com/in/noya-adivi/"><img src="https://img.shields.io/badge/LinkedIn-DAD5FF?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzU1NDhDOCIgZD0iTTIwLjQ1IDIwLjQ1aC0zLjU2di01LjU3YzAtMS4zMy0uMDMtMy4wNC0xLjg1LTMuMDQtMS44NiAwLTIuMTQgMS40NS0yLjE0IDIuOTR2NS42N0g5LjM1VjloMy40MXYxLjU2aC4wNWMuNDgtLjkgMS42NC0xLjg1IDMuMzctMS44NSAzLjYgMCA0LjI3IDIuMzcgNC4yNyA1LjQ2djYuMjh6TTUuMzQgNy40M2EyLjA2IDIuMDYgMCAxIDEgMC00LjEzIDIuMDYgMi4wNiAwIDAgMSAwIDQuMTN6TTcuMTIgMjAuNDVIMy41NlY5aDMuNTZ2MTEuNDV6TTIyLjIyIDBIMS43N0MuNzkgMCAwIC43NyAwIDEuNzN2MjAuNTRDMCAyMy4yMy43OSAyNCAxLjc3IDI0aDIwLjQ1Yy45OCAwIDEuNzgtLjc3IDEuNzgtMS43M1YxLjczQzI0IC43NyAyMy4yIDAgMjIuMjIgMHoiLz48L3N2Zz4=" alt="LinkedIn"></a>
  <a href="https://noyaadivi.github.io/noya-website"><img src="https://img.shields.io/badge/%D7%AA%D7%99%D7%A7_%D7%A2%D7%91%D7%95%D7%93%D7%95%D7%AA-D9F3E7?style=for-the-badge&logo=githubpages&logoColor=1F7350" alt="תיק עבודות"></a>
  <a href="https://github.com/NoyaAdivi"><img src="https://img.shields.io/badge/%D7%A2%D7%95%D7%93_%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98%D7%99%D7%9D-FBD5E0?style=for-the-badge&logo=github&logoColor=A03A5C" alt="עוד פרויקטים"></a>
</p>

</div>
