# cross_regulation_pipeline
Project is dedicated to the searching for cross-regulatory pathways in NMD

## Logic  of Data Analysis
* [eCLIP] &#8596; [**factor** should have peak (binding site) in **target** ]
* [inactivation of NMD] &#8596; **poison exons** of **target** &#0916;&#0936; > 0
                         & **essential exons** of **target** &#0916;&#0936; < 0
* [shRNA-KD of factor] &#8596; **factor** may:
  - activate inclusion of poison exon &#8596; (&#0916;&#0936; < 0) & &#8593;NMD
  - repress inclusion of poison exon &#8596; (&#0916;&#0936; > 0) & &#8595;NMD
  - activate inclusion of essential exon &#8596; (&#0916;&#0936; < 0) & &#8595;NMD
  - repress inclusion of essential exon &#8596; (&#0916;&#0936; > 0) & &#8593;NMD
  
