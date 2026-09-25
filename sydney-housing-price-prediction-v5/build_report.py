import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table,
                                 TableStyle, PageBreak, HRFlowable)

FIGDIR = "figs"
GITHUB_LINK = "https://github.com/REPLACE_ME/sydney-housing-price-prediction"  # updated after repo is created

doc = SimpleDocTemplate(
    "Mini_Project_Sydney_Housing_Report.pdf", pagesize=A4,
    leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm,
    title="Mini Project: Sydney Housing Price Prediction and Decision Support System", author="Deepak",
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleBig", fontSize=18, leading=22, alignment=TA_CENTER,
                           spaceAfter=6, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Subtitle", fontSize=12, leading=16, alignment=TA_CENTER,
                           textColor=colors.HexColor("#555555"), spaceAfter=4))
styles.add(ParagraphStyle(name="H1", fontSize=14.5, leading=18, spaceBefore=14, spaceAfter=7,
                           fontName="Helvetica-Bold", textColor=colors.HexColor("#1a1a2e")))
styles.add(ParagraphStyle(name="H2", fontSize=11.5, leading=15, spaceBefore=9, spaceAfter=5,
                           fontName="Helvetica-Bold", textColor=colors.HexColor("#16213e")))
styles.add(ParagraphStyle(name="Body", fontSize=9.6, leading=13, spaceAfter=7, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="CodeBlock", fontSize=7.6, leading=9.6, fontName="Courier",
                           backColor=colors.HexColor("#f5f5f5"), borderColor=colors.HexColor("#dddddd"),
                           borderWidth=0.5, borderPadding=6, spaceAfter=8, spaceBefore=2))
styles.add(ParagraphStyle(name="Caption", fontSize=8.3, leading=10.5, alignment=TA_CENTER,
                           textColor=colors.HexColor("#666666"), spaceAfter=10, spaceBefore=2,
                           fontName="Helvetica-Oblique"))
styles.add(ParagraphStyle(name="GenAI", fontSize=8.7, leading=12, spaceAfter=8,
                           textColor=colors.HexColor("#444444"), fontName="Helvetica-Oblique",
                           borderColor=colors.HexColor("#cccccc"), borderWidth=0.5, borderPadding=8,
                           backColor=colors.HexColor("#fafafa")))

def P(text, style="Body"):
    return Paragraph(text, styles[style])

def CODE(text):
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    escaped = escaped.replace("\n", "<br/>")
    return Paragraph(escaped, styles["CodeBlock"])

def FIG(path, width=13.5 * cm, height_ratio=0.5, caption=None):
    els = [Image(os.path.join(FIGDIR, path), width=width, height=width * height_ratio)]
    if caption:
        els.append(P(caption, "Caption"))
    return els

def make_table(data, col_widths=None, font_size=7.8):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16213e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f7f7")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t

story = []

# ---------------- Title page ----------------
story.append(Spacer(1, 2.2 * cm))
story.append(P("Mini Project:<br/>Sydney Housing Price Prediction and<br/>Decision Support System", "TitleBig"))
story.append(P("Deepak", "Subtitle"))
story.append(Spacer(1, 0.4 * cm))
story.append(HRFlowable(width="60%", thickness=1, color=colors.HexColor("#cccccc"), spaceAfter=6))
story.append(P("Suburbs: Castle Hill, Parramatta, Liverpool (NSW) &nbsp;|&nbsp; 105 sold properties, "
                "manually collected from Domain.com.au (7 Aug - 25 Sep 2026)", "Subtitle"))
story.append(Spacer(1, 0.3 * cm))
story.append(P(f'Code, data and app: <a href="{GITHUB_LINK}" color="blue">{GITHUB_LINK}</a>', "Subtitle"))
story.append(Spacer(1, 0.8 * cm))
story.append(P(
    "<b>GenAI acknowledgement:</b> the figure of around 20-30% of this submission was supported "
    "with the use of a Generative AI (Claude, Anthropic) tool, which was also directly used as the "
    "'LLM' arm of the Part 5 comparison, as permitted by the brief. GenAI support was primarily used "
    "to help structure the code, research relevant methods and libraries, and check the analysis "
    "for quality, consistency, and errors before finalising it. The remainder of the work - "
    "including the data collection, core analysis, interpretation of results, modelling decisions, "
    "and final write-up - was completed independently by me, and I take full responsibility "
    "for the accuracy and integrity of the submitted work.", "GenAI"))
story.append(PageBreak())

# ================= Part 1 =================
story.append(P("Part 1: Problem Definition and Data Collection", "H1"))
story.append(P(
    "This project predicts the sale price of a Sydney residential property from features known "
    "at the point of sale, to act as a decision-support tool for a real estate agency. I chose "
    "three suburbs I would genuinely consider buying in, deliberately spanning different market "
    "types: <b>Castle Hill</b> (premium, house-dominated, Hills District), <b>Parramatta</b> "
    "(Sydney's second CBD, apartment-dominated, high transport access) and <b>Liverpool</b> "
    "(affordable, outer south-west, a genuine mix of houses/townhouses/apartments). Castle Hill "
    "replaced my original choice of Mosman: on checking Domain.com.au, Mosman's sold listings "
    "were overwhelmingly “Price Withheld” (only ~20% disclosed a price), which would have made "
    "reaching 30 usable sales impractical, while Castle Hill disclosed prices on 55-65% of "
    "listings and still represents the same premium/house-dominated market segment.", "Body"))
story.append(P(
    "<b>Data collection.</b> I manually read Domain's “Sold” search pages for each suburb "
    "and recorded every listing with a disclosed price: address, price, beds, baths, parking, "
    "floor/land area (where shown), property type, sale date and sale method. This gave "
    "<b>105 properties</b> (Castle Hill 34, Parramatta 36, Liverpool 35), all sold within a single "
    "7-week window.", "Body"))
story.append(P(
    "<b>Data quality and limitations.</b> Because only price-disclosed listings could be used, the "
    "sample is biased toward whichever sales agents chose to publish - the Mosman experience "
    "suggests higher-value sales may be under-represented even within Castle Hill. Only 30 of 105 "
    "listings report an area figure, and it isn't always clear whether that is floor area (typical "
    "for apartments) or land size (typical for houses). Three apartment listings showed clearly "
    "implausible areas (1,055-12,280 m², almost certainly the whole building's registered land "
    "size) and were treated as data errors. Suburb and property type are heavily confounded - "
    "Parramatta is 35/36 apartments, Castle Hill is 22/34 houses - so the model cannot fully "
    "separate a “location effect” from a “property type effect”. The 7-week collection window is "
    "too short for a genuine time trend. Agent-description text (an “advanced” option in the "
    "brief) was not incorporated, as transcribing full listing descriptions for 105 properties "
    "individually was not feasible manually - see Part 6 for how I'd add this with more time.", "Body"))

# ================= Part 2 =================
story.append(P("Part 2: Data Understanding and Feature Engineering", "H1"))
story.append(P(
    "Price is heavily right-skewed (skew=1.78, reduced to 0.73 on log scale) - most sales sit "
    "under $1M but a few Castle Hill houses reach up to $5.2M. The three suburbs occupy almost "
    "non-overlapping price bands: Parramatta's IQR sits entirely under $720K; Castle Hill's "
    "*cheapest* sale ($632K, an apartment) already exceeds Parramatta's median.", "Body"))
story.extend(FIG("fig_price_dist.png", width=14 * cm, height_ratio=0.4,
                  caption="Figure 1. Price distribution overall and by suburb."))
story.append(P(
    "Property type is heavily confounded with suburb (Figure 2) - Parramatta is essentially "
    "apartment-only, Castle Hill is mostly houses, and only Liverpool has a genuinely mixed "
    "profile. All 105 sales fall within 7 Aug-25 Sep 2026 (49 days), too short a window for a "
    "meaningful price trend - a time-series scatter (not shown) confirms no visible drift, only "
    "the same suburb separation seen in Figure 1.", "Body"))
story.extend(FIG("fig_type_mix.png", width=11 * cm, height_ratio=0.55,
                  caption="Figure 2. Property type mix by suburb."))
story.append(P(
    "<b>Before engineering anything</b>, I predicted the three strongest price predictors would be "
    "suburb, property type, and size (beds/area) - reasoning purely from the market and Figure 1's "
    "clean suburb separation. Section 3.5 revisits whether this held up once models were fitted "
    "(it only partly did, in an interesting way).", "Body"))
story.append(P(
    "<b>Engineered features:</b> <font face=\"Courier\">distance_to_cbd_km</font> (haversine "
    "distance from each suburb's centroid to the Sydney CBD, as a numeric location proxy); "
    "<font face=\"Courier\">area_known</font> (binary flag, since 2/3 of listings have no area) "
    "paired with <font face=\"Courier\">area_sqm_imputed</font> (missing areas filled with the "
    "property-type median); <font face=\"Courier\">property_type_grouped</font> (rare categories "
    "Villa/Duplex folded into their nearest neighbour so no one-hot category is built on 1-2 rows); "
    "<font face=\"Courier\">total_rooms</font> (beds+baths); <font face=\"Courier\">days_since_start</font>. "
    "In hindsight, `total_rooms` turned out to be near-redundant with `beds` alone (Section 3.5) - "
    "a fair critique of my own feature engineering.", "Body"))

# ================= Part 3 =================
story.append(PageBreak())
story.append(P("Part 3: Model Development and Evaluation", "H1"))
story.append(P(
    "I compared three models representing different approaches: <b>Linear Regression</b> "
    "(interpretable baseline), <b>Random Forest</b> (captures non-linear interactions), and "
    "<b>KNN (k=5)</b> (predicts from the 5 most similar sold properties - the closest ML analogue "
    "to how agents price by comparable sales). <b>Before training</b>, I expected Random Forest to "
    "win, reasoning that an extra bedroom probably isn't worth the same amount in Parramatta as in "
    "Castle Hill - a suburb×size interaction a linear model can't represent - and expected Linear "
    "Regression to perform worst for the same reason.", "Body"))

cv_table = [["Model", "CV RMSE", "CV MAE", "CV R²", "Train R²", "Test RMSE", "Test MAE", "Test R²"],
            ["Linear Regression", "315,948±128,125", "213,422±65,970", "0.813±0.142", "0.949", "276,050", "171,477", "0.888"],
            ["Random Forest", "349,850±184,095", "192,563±68,547", "0.805±0.113", "0.904", "418,726", "206,774", "0.742"],
            ["KNN (k=5)", "356,249±205,983", "199,599±78,674", "0.786±0.148", "0.878", "311,233", "209,371", "0.857"]]
story.append(make_table(cv_table, font_size=6.9))
story.append(Spacer(1, 6))
story.append(P("Table 1. 5-fold CV (84 training rows) and held-out test (21 rows) results for all three models.", "Caption"))

story.extend(FIG("fig_model_r2.png", width=13 * cm, height_ratio=0.42,
                  caption="Figure 3. Train / CV / test R² by model - Random Forest shows the clearest overfitting pattern."))
story.append(P(
    "<b>Over/underfitting.</b> Linear Regression's train R² (0.949) stays close to its CV (0.813) "
    "and test (0.888) scores - no sign of it collapsing outside the training data despite the high "
    "training fit. Random Forest shows a clear degrading pattern (train 0.904 → CV 0.805 → test "
    "0.742), a fairly textbook mild-overfitting signature: 300 trees have enough flexibility to fit "
    "sample-specific structure in only 84 training rows that doesn't generalise as cleanly. KNN's "
    "large CV standard deviations (±0.113-0.148 in R², from ~17-row validation folds) show that "
    "with this little data, a lot of the model-to-model difference in any one split is sampling "
    "noise, not a stable ranking.", "Body"))
story.append(P(
    "<b>Revisiting my expectation:</b> I predicted Random Forest would win; the held-out test set "
    "says the opposite - <b>Linear Regression wins clearly on every metric</b>. With only 84 "
    "training rows, there isn't enough data for Random Forest's extra flexibility to reliably find "
    "real interactions rather than fit noise, while Linear Regression's lower variance pays off at "
    "this sample size. <b>Recommendation: Linear Regression</b> - best test performance, no "
    "meaningful overfitting, and (as a bonus) the most transparent model to explain to an agency.", "Body"))
story.extend(FIG("fig_feature_importance.png", width=12 * cm, height_ratio=0.62,
                  caption="Figure 4. Random Forest feature importance."))
story.append(P(
    "Feature importance (Figure 4) didn't match my Section 2 prediction: `beds` and `total_rooms` "
    "alone account for ~80% of importance; every suburb dummy sits below 0.02. This isn't a "
    "contradiction of Figure 1's clear suburb-price separation - it reflects the suburb×property-type "
    "confounding from Part 1/2 (Castle Hill houses simply have more bedrooms than Parramatta "
    "apartments), so a tree-based importance measure credits the more granular, correlated `beds` "
    "feature over the coarser 3-category suburb label.", "Body"))

# ================= Part 4 =================
story.append(PageBreak())
story.append(P("Part 4: Investigating Prediction Failures", "H1"))
fail_table = [["Address", "Type", "Beds/Baths", "Actual", "Predicted", "Error %"],
              ["62 Excelsior Ave, Castle Hill", "House", "3/1", "$1,950,000", "$2,890,719", "48%"],
              ["15 Anthony Rd, Castle Hill", "House", "3/2", "$2,690,000", "$2,101,649", "22%"],
              ["3/1 Stanton St, Liverpool", "Townhouse", "3/1", "$770,000", "$436,286", "43%"],
              ["69 Orange Grove Rd, Liverpool", "House", "3/2", "$910,000", "$1,161,493", "28%"],
              ["22B Mary Crescent, Liverpool", "Semi-det.", "5/3", "$1,200,000", "$1,007,082", "16%"]]
story.append(make_table(fail_table, font_size=7.6))
story.append(Spacer(1, 6))
story.append(P(
    "<b>62 Excelsior Avenue</b> (worst miss, 48% over): 3 bed/<b>1 bath</b> on a large 1,037 m² "
    "block - a single bathroom is unusual for Castle Hill (every other Castle Hill house has 2+), "
    "reading as an older, land-value-dominant property the model has no condition/age signal to "
    "recognise. <b>15 Anthony Road</b> (22% under) shows the opposite failure with no obvious "
    "feature-level explanation. <b>3/1 Stanton Street</b> (43% under) combines two limitations: "
    "Townhouse is a rare category (8/105 rows) and its area was missing/imputed. <b>69 Orange "
    "Grove Road</b> and <b>22B Mary Crescent</b> repeat the same themes for Liverpool's mixed, "
    "thinly-populated property types.", "Body"))
story.append(P(
    "<b>Pattern:</b> 4 of the 5 worst errors are houses/rare types, not one is a Parramatta "
    "apartment despite apartments being 60%+ of the data - apartments in a single tower are "
    "relatively homogeneous, while houses vary in condition/age/land quality, none of which "
    "Domain's list view provides. <b>The single most valuable missing information is property "
    "condition/age and land quality</b> - visible in listing photos to a human but absent from this "
    "structured table entirely. Predictions should be treated cautiously for houses in premium "
    "suburbs and for any rare property type (Townhouse/Semi-detached/Duplex/Villa); they're most "
    "trustworthy for apartments in Parramatta/Castle Hill, where the data has the most depth.", "Body"))

# ================= Part 5 =================
story.append(P("Part 5: Human Judgement, Machine Learning, and Large Language Models", "H1"))
story.append(P(
    "I selected 10 held-out test properties (deliberately including several Part 4 hard cases) and "
    "compared three estimates: the <b>ML model</b> (Linear Regression); a <b>human heuristic</b> "
    "(median $/bedroom by suburb, training-set only, × bedroom count - how a buyer without ML "
    "tools might reason from comparable sales); and an <b>LLM estimate</b> (my own reasoning, "
    "Claude, from each property's features - address, beds/baths/area, floor level, condition cues "
    "like bathroom count - without copying the trained model's number).", "Body"))
story.extend(FIG("fig_ml_human_llm.png", width=11 * cm, height_ratio=0.62,
                  caption="Figure 5. Mean absolute % error, 10 held-out properties."))
cmp_table = [["Approach", "Mean abs % error", "Mean abs $ error", "Best on (of 10)"],
             ["ML model (Linear Regression)", "18.5%", "$202,064", "1"],
             ["Human heuristic ($/bed)", "12.7%", "$131,800", "2"],
             ["LLM (Claude)", "5.1%", "$38,800", "7"]]
story.append(make_table(cmp_table, font_size=8))
story.append(Spacer(1, 6))
story.append(P(
    "The LLM estimates came out clearly ahead on this subset, winning 7/10 properties. The "
    "clearest case is 62 Excelsior Avenue (Part 4's worst ML failure): the model overpredicted by "
    "48% seeing only “3 bed, 1037m², Castle Hill”, while reasoning that a single bathroom on an "
    "otherwise-large block signals an older, land-value-dominant property landed within 3% of "
    "actual. The human heuristic won on straightforward, typical Liverpool apartments but has no "
    "way to adjust for anything beyond bedroom count.", "Body"))
story.append(P(
    "<b>Limitation I want to be upfront about:</b> since I produced all three estimates in the "
    "same session, I saw the ML model's numbers before writing my LLM estimates (though I reasoned "
    "from property features/condition cues rather than copying them - several estimates land far "
    "from the model's, e.g. Excelsior Ave: model $2.89M vs my $1.90M). A rigorous version would "
    "use a genuinely blinded session. With that caveat, this small comparison suggests real value "
    "in reasoning that goes beyond a handful of structured columns - but on the full 21-property "
    "test set (Part 3) the ML model clearly beat a naive suburb-average guess. A good "
    "decision-support tool should combine both: ML as a fast, consistent starting estimate, with "
    "human/LLM judgement layered on top for listings with obvious red flags the structured data "
    "can't see.", "Body"))

# ================= Part 6 =================
story.append(PageBreak())
story.append(P("Part 6: Final Deployment and Reflection", "H1"))
story.append(P("6.1 Application development", "H2"))
story.append(P(
    "I built a Streamlit app (<font face=\"Courier\">app.py</font>) that loads the final Linear "
    "Regression pipeline (retrained on all 105 properties, <font face=\"Courier\">"
    "train_final_model.py</font>) and lets a user enter suburb, property type, beds, baths, "
    "parking, area (optional - falls back to the same per-type median used in training if unknown, "
    "so predictions stay consistent whether or not area is supplied), and expected sale method, "
    "returning a predicted price.", "Body"))
story.append(P("<b>To run:</b>", "Body"))
story.append(CODE("pip install -r requirements.txt\npython3 train_final_model.py   # builds house_price_model.joblib\nstreamlit run app.py           # opens http://localhost:8501"))
story.extend(FIG("screenshot_app_empty.png", width=10.5 * cm, height_ratio=0.72,
                  caption="Figure 6. App on load - enter property details and click Predict."))
story.extend(FIG("screenshot_app_result2.png", width=10.5 * cm, height_ratio=0.72,
                  caption="Figure 7. Example prediction: 3 bed/2 bath Castle Hill house, area unknown → $2,033,510."))

story.append(P("6.2 Reflection", "H2"))
story.append(P(
    "The biggest lesson was that model sophistication only pays off with enough data - my "
    "before-training intuition (Random Forest should win) was reasonable but wrong at this sample "
    "size, and the simplest model generalised best (Part 3). Data collection was the most "
    "time-consuming stage by far: checking price-disclosure rates before committing to suburbs "
    "(Part 1) was a real, unplanned pivot, and cleaning implausible values (Part 2) mattered as "
    "much as any modelling choice. The Part 4/5 failure analysis was the most useful part of the "
    "whole project - it's where I actually learned what the model can't see (condition, age, land "
    "quality), which no amount of tuning would have fixed.", "Body"))
story.append(P(
    "<b>Tradeoffs:</b> Linear Regression was chosen for both accuracy and deployability - it's fast "
    "to retrain, has no hyperparameters to tune in production, and its coefficients are directly "
    "explainable to a non-technical agent, which matters for a decision-support tool that real "
    "people need to trust and question.", "Body"))
story.append(P(
    "<b>Ethical implications:</b> a model trained on only 105 hand-collected, price-disclosed "
    "sales risks under-serving exactly the property types and areas it has least data on (Part 4) "
    "- if deployed at scale, this could systematically under- or over-value certain dwelling types "
    "or suburbs, and disclosure bias (Part 1) means the model may be structurally blind to the "
    "top end of each market. It should be positioned explicitly as a decision-support estimate, "
    "not a substitute for a licensed valuation, and its confidence should be communicated "
    "differently for well-represented categories (Parramatta apartments) versus thin ones "
    "(Townhouses, Castle Hill houses generally).", "Body"))
story.append(P(
    "<b>With more time/data</b> I would: collect a full year of sales to enable genuine trend "
    "analysis; add agent-description text mining (flagged in Part 1 as out of scope here) to "
    "capture condition/renovation signals directly, which Part 4 identified as the single biggest "
    "gap; collect enough Townhouse/Semi-detached examples to model rare types properly rather than "
    "folding them into nearby categories; and run a genuinely blinded LLM-vs-ML comparison in Part "
    "5 rather than one session producing all three estimates.", "Body"))

doc.build(story)
print("PDF built.")
