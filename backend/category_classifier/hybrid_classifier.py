import pandas as pd
import numpy as np
from typing import List
import time
import os
import sys

# === Blacklist terms that override anything to "אחר" ===
BLACKLIST_TERMS = [
    "שמפו",
    "סבון",
    "מברשת",
    "מנוע",
    "קרם גוף",
    "אקונומיקה",
    "חיתול",
    "שואב",
    "תמיסה",
    "תחבושת",
    "שפתון",
    "דאודורנט",
]

# === Rule-based category keywords ===
CATEGORY_KEYWORDS = {
    "חלב וגבינות": [
        "חלב",
        "יוגורט",
        "גבינה",
        "שמנת",
        "קוטג",
        "חמאה",
        "ריקוטה",
        "פרמזן",
    ],
    "פסטה ואטריות": ["פסטה", "ספגטי", "לזניה", "אטריות", "מקרוני", "פתיתים", "טליאטלה"],
    "ממתקים וחטיפים": ["שוקולד", "במבה", "ביסלי", "עוגיה", "חטיף", "סוכריה"],
    "משקאות": ["מים", "קולה", "מיץ", "קפה", "תה", "בירה", "יין", "וודקה"],
    "בשר ודגים": ["עוף", "שניצל", "בשר", "דג", "נקניק", "פסטרמה", "סלמון"],
    "מאפים ולחמים": ["לחם", "פיתה", "חלה", "עוגה", "עוגיות", "לחמניה"],
    "פירות וירקות": ["עגבניה", "מלפפון", "בננה", "תפוח", "גזר", "בצל", "חסה"],
}


# === Rule-based classification ===
def rule_based_classify(name: str) -> str:
    name = str(name).lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in name for word in keywords):
            return category
    return "אחר"


# === Blacklist override ===
def is_blacklisted(name: str) -> bool:
    name = str(name).lower()
    return any(term in name for term in BLACKLIST_TERMS)


# === Semantic classifier using FAISS + sentence-transformers ===
class HebrewProductClassifier:
    def __init__(self):
        from sentence_transformers import SentenceTransformer
        import faiss

        print("Loading language model...")
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

        self.category_examples = {
            "בשר ודגים": [
                "בשר בקר טחון",
                "עוף שלם טרי",
                "דג סלמון קפוא",
                "פסטרמה הודו מעושנת",
                "נקניק מעושן",
                "טונה בשמן זית",
                "שניצל עוף פירורי לחם",
                "קבב טלה טחון",
                "פילה דג לבן",
                "בשר כבש צלוי",
                "עוף בבישול ביתי",
                "דג טרי מהים",
                "קציצות בשר בקר",
                "סלמון מעושן",
                "בשר עגל רך",
                "דג טונה טרי",
                "נתחי עוף",
                "בשר הודו",
                "דגי ים",
                "עוף אורגני",
            ],
            "חלב וגבינות": [
                "חלב 3% שומן טרי",
                "גבינה צהובה קשה",
                "יוגורט יווני עבה",
                "שמנת חמוצה 15%",
                "מוצרלה טרייה רכה",
                "קוטג' 5% שומן",
                "גבינת עיזים מיושנת",
                "פטה בולגרית מלוחה",
                "חמאה מתוקה",
                "קרם שמנת מתוקה",
                "גבינה לבנה רכה",
                "חלב שקדים טבעי",
                "יוגורט ביו פרו",
                "גבינת שמנת",
                "גבינה מגורדת",
                "חלב ללא לקטוז",
                "גבינת צ'דר",
                "ריקוטה",
                "גבינת פרמזן",
                "שמנת מתוקה",
            ],
            "פירות וירקות": [
                "תפוח אדום טרי",
                "בננה בשלה מתוקה",
                "גזר אורגני צעיר",
                "בצל צהוב בינוני",
                "עגבניות שרי מתוקות",
                "מלפפון חמוץ ארוך",
                "חסה קרחון פריכה",
                "תפוח אדמה לבן",
                "תפוז סחוט טבעי",
                "אבוקדו בשל",
                "פלפל אדום מתוק",
                "ברוקולי טרי ירוק",
                "תפוח אדמה סגול",
                "בטטה כתומה",
                "חציל ארוך",
                "קישוא ירוק",
                "כרוב לבן",
                "תרד עלים",
                "פטרוזיליה טרייה",
                "שום לבן",
            ],
            "לחם ומאפים": [
                "לחם קמח מלא",
                "חלה שבת קלועה",
                "פיתה ערבית",
                "לחמנייה המבורגר רכה",
                "קרואסון חמאה צרפתי",
                "עוגת שוקולד ביתית",
                "בגט צרפתי פריך",
                "מאפה גבינה מלוח",
                "עוגיות שיבולת שועל",
                "קרקרים מלוחים",
                "וופל בלגי מתוק",
                "לחם שיפון כהה",
                "פיתה מקמח מלא",
                "עוגת דבש",
                "לחמנייה מתוקה",
                "מצות שמורה",
                "עוגיות חמאה",
                "קייק וניל",
                "מאפה שוקולד",
                "לחם פומפרניקל",
            ],
            "פסטה ואטריות": [
                "ספגטי דורום",
                "פן צבעוני תלת צבע",
                "לזניה טרייה",
                "מקרוני קצר",
                "פטוצ'יני רחב שטוח",
                "אטריות אורז דקות",
                "ריזוטו ארבוריו",
                "קוסקוס דק",
                "אטריות סובה יפניות",
                "פסטה אינטגרלית",
                "טליאטלה ביצים",
                "פארפלה פרפר",
                "פני ברונזה",
                "ריגטוני חלול",
                "קונקיליה צדפים",
                "אניולוטי ממולא",
            ],
            "שימורים": [
                "שימורי תירס מתוק",
                "רסק עגבניות איטלקי",
                "טונה בשמן זית",
                "שעועית לבנה מבושלת",
                "פלפל צלוי אדום",
                "זיתים ירוקים ממולאים",
                "עגבניות מרוסקות",
                "תירס בגרעינים צהובים",
                "שימורי אפרסק בסירופ",
                "רוטב מרינרה מוכן",
                "שעועית אדומה מתובלת",
                "חומוס מוכן",
                "זיתים שחורים",
                "רוטב עגבניות",
                "פלפלים חריפים",
                "לב דקל",
            ],
            "משקאות": [
                "מים מינרלים טבעיים",
                "קולה דיאט ללא סוכר",
                "מיץ תפוזים טבעי סחוט",
                "בירה טובורג",
                "יין אדום יבש",
                "קפה אספרסו איטלקי",
                "תה ירוק סיני",
                "משקה אנרגיה",
                "מים עם גז",
                "לימונדה טבעית",
                "משקה איזוטוני ספורט",
                "מיץ ענבים לבן",
                "בירה חיטה",
                "וודקה רוסית",
                "וויסקי סקוטי",
                "ברנדי יווני",
            ],
            "ממתקים וחטיפים": [
                "שוקולד חלב מילקה",
                "ממתקי גומי צבעוניים",
                "ביסלי פיצה",
                "במבה אגוזי לוז",
                "עוגיות אוראו שחור לבן",
                "חטיף אנרגיה פירות",
                "וופל שוקולד נוטלה",
                "מרשמלו לבן",
                "סוכריות קשות פירות",
                "דבש דבורים טבעי",
                "ריבת תות ביתית",
                "פסק זמן שוקולד",
                "קליק חלב",
                "מקופלת אגוזים",
                "חטיף גרנולה",
                "פופקורן מלוח",
            ],
            "שמנים וחומצים": [
                "שמן זית אקסטרה בתולי",
                "שמן חמניות מזוכך",
                "שמן קנולה בריא",
                "חומץ בלסמי איטלקי",
                "שמן קוקוס טבעי",
                "חומץ יין לבן",
                "שמן אגוזים קלויים",
                "שמן שומשום קלוי",
                "שמן תירס",
                "שמן זית ספרדי",
                "חומץ תפוחים",
                "שמן פשתן",
            ],
            "תבלינים ובישול": [
                "מלח ים גס",
                "פלפל שחור טחון",
                "כמון טחון עדין",
                "פפריקה מעושנת מתוקה",
                "אורגנו יבש יווני",
                "קינמון אמיתי קלוי",
                "כורכום טהור הודי",
                "בזיליקום טרי ירוק",
                "שום כתוש טרי",
                "רוזמרין יבש",
                "זעתר הרים",
                "מיונז ביתי",
                "חרדל דיז'ון",
                "קטשופ עגבניות",
                "רוטב סויה",
                "מלח שחור הודי",
            ],
            "מוצרי ניקוי": [
                "דטרגנט כביסה אבקה",
                "סבון כלים לימון",
                "מרכך בגדים ריח",
                "חומר ניקוי רצפות אמוניה",
                "סבון רחצה לבנדר",
                "שמפו לשיער יבש",
                "נייר טואלט רך",
                "מטליות לחות מכלים",
                "אקונומיקה כביסה",
                "ג'ל רחצה",
                "משחת שיניים",
                "מחטא רצפות",
            ],
            "קפואים": [
                "ירקות קפואים מעורבים",
                "פיצה קפואה מרגריטה",
                "גלידת וניל איטלקית",
                "דגים קפואים ללא עצמות",
                "פירות יער קפואים",
                "פרנצ'יפריי קפוא",
                "קציצות קפואות בשר",
                "לזניה קפואה",
                "שניצל קפוא",
                "ירקות וק אסיאתיים",
                "עוגת קפה קפואה",
                "דגי סלמון קפואים",
            ],
            "קטניות ודגנים": [
                "אורז בסמטי ארוך",
                "קינואה אדומה",
                "עדשים כתומות מקולפות",
                "חומוס יבש גדול",
                "שעועיות כליה אדומות",
                "פול ירוק יבש",
                "שיבולת שועל גליל",
                "בורגול גס",
                "אורז ארבוריו איטלקי",
                "עדשים שחורות",
                "פול לימה",
                "שעועית לוביה",
            ],
            "אחר": ["מוצר לא מזוהה", "פריט כללי", "דבר לא ברור", "חפץ לא מסווג"],
        }  # Use the full example block from original file
        self._setup_fast_search()

    def _setup_fast_search(self):
        import faiss

        all_examples = []
        self.example_to_category = {}
        for category, examples in self.category_examples.items():
            for example in examples:
                all_examples.append(example)
                self.example_to_category[example] = category

        embeddings = self.model.encode(all_examples, show_progress_bar=True)
        embeddings = embeddings.astype("float32")
        faiss.normalize_L2(embeddings)

        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
        self.all_examples = all_examples

    def classify_batch(self, products: List[str]) -> List[str]:
        import faiss

        clean_products = [str(p) if p and not pd.isna(p) else "" for p in products]
        embeddings = self.model.encode(clean_products, show_progress_bar=False)
        embeddings = embeddings.astype("float32")
        faiss.normalize_L2(embeddings)
        similarities, indices = self.index.search(embeddings, k=3)

        results = []
        for i, (sims, idxs) in enumerate(zip(similarities, indices)):
            if clean_products[i] == "":
                results.append("אחר")
            elif sims[0] > 0.82:
                category = self.example_to_category[self.all_examples[idxs[0]]]
                results.append(category)
            else:
                results.append("אחר")
        return results

    def classify_products(
        self, df: pd.DataFrame, name_column: str = "name", batch_size: int = 1000
    ) -> pd.DataFrame:
        products = df[name_column].tolist()
        all_categories = []
        for i in range(0, len(products), batch_size):
            batch = products[i : i + batch_size]
            batch_categories = self.classify_batch(batch)
            all_categories.extend(batch_categories)
        df = df.copy()
        df["category"] = all_categories
        return df


# === Hybrid classification ===
def hybrid_classify(df: pd.DataFrame, name_col: str = "name") -> pd.DataFrame:
    df = df.copy()
    df["category"] = df[name_col].apply(rule_based_classify)
    to_classify = df[df["category"] == "אחר"].copy()

    if not to_classify.empty:
        print(f"→ {len(to_classify)} products need semantic classification")
        classifier = HebrewProductClassifier()
        classified = classifier.classify_products(to_classify, name_column=name_col)

        def postprocess(row):
            if is_blacklisted(row[name_col]):
                return "אחר"
            return row["category"]

        classified["category"] = classified.apply(postprocess, axis=1)
        df.loc[classified.index, "category"] = classified["category"]

    return df


# === Example usage ===
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "name": [
                "חלב תנובה 3%",
                "פסטה ברילה",
                "מיץ תפוזים טבעי",
                "עוף שלם קפוא",
                "ביסלי גריל",
                "קרם גוף וניל",
                "מברשת אסלה",
                "יוגורט עיזים 4.5%",
                "טונה בשמן זית",
            ]
        }
    )

    result_df = hybrid_classify(df)
    print("\n📊 Categorized Products:")
    print(result_df.to_string(index=False))
