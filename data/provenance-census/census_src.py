"""The provenance census, first batch (2026-10-29). Writes census.json.

Every quoted value is checked verbatim (whitespace-normalised) against the saved text of its source in sources/,
which manifest.json dates and hashes. Fields without a quote are readings, marked basis "reading".
Capability is recorded as what a resource expresses, records or tests; an untested capability is "not tested",
never a failure."""
import json, pathlib, re
HERE = pathlib.Path(__file__).parent
MAN = json.load(open(HERE / "sources/manifest.json"))

def Q(src, quote, basis="operator"):
    return {"src": src, "basis": basis, "quote": quote}

ROWS = []
def row(**r): ROWS.append(r)

# ---------------------------------------------------------------- IPTC
row(slug="iptc-photo-metadata-tests", name="IPTC photo metadata tests", aka=["IPTC Social Media Sites Photo Metadata Test Results", "IPTC Photo Metadata Research"],
    url="https://iptc.org/standards/photo-metadata/research/", operator="IPTC (International Press Telecommunications Council), Photo Metadata Working Group",
    lineage="media", kind="test series",
    capability=["expresses", "tests"],
    provenance_object="the photograph as a file: embedded Exif and IPTC metadata (IIM and XMP)",
    relation_types=["creation (creator)", "credit", "rights (copyright notice)", "description (caption)"],
    provenance_carrier="embedded metadata inside the image file",
    unit="a site or system, tested by upload and by saving or downloading the uploaded image",
    transformations_tested=["upload to a sharing site or system", "display to a viewer", "Save As from the browser", "download through the system"],
    retention_results="2019: of eleven image-sharing sites, Pexels, pixabay and Unsplash stripped metadata from saved and downloaded files; Flickr replaced the embedded creator with the account owner; Flickr's saved files had no XMP, EyeEm's no Exif and Google Photo's no IPTC IIM; Behance's saved files kept the embedded metadata; among file and message systems Twitter stripped it on Save As, Dropbox and Microsoft OneDrive previews saved with the metadata stripped, Facebook kept a few rights fields in IIM and Exif",
    cadence="periodic: 2013, 2016, Spring 2019 (the 2019 page); a software test published August 2014",
    count={"value": "15 social media sites tested in 2016 and 2013 (research page); about a dozen checked regularly (2019 page)", "as_of": "2019"},
    lifecycle={"state": "historical", "detail": "dated results; the 2019 table is not a 2026 platform measurement. Succeeded in method by Metawatch (2026)"},
    version_and_time={"results": "Spring 2019", "earlier": "2013, 2016", "software_study": "August 2014", "read": "2026-10-29"},
    negative_tags=["NOT a current platform audit: each table carries its test year", "NOT a test of C2PA credentials"],
    evidence={
      "self_description": Q("iptc-photo-metadata-tests--social-2019", "IPTC promotes the proper use of IPTC Photo Metadata and claims “embedded metadata should not be removed” from images shared on a photo platform or a system for sharing files or messages with images."),
      "cadence": Q("iptc-photo-metadata-tests--social-2019", "IPTC checks about a dozen sites regularly: in 2013, in 2016 and now again in Spring 2019"),
      "count": Q("iptc-photo-metadata-tests--research", "The IPTC Photo Metadata Working Group tested 15 social media sites in 2016 and 2013"),
      "transformations_tested": Q("iptc-photo-metadata-tests--social-2019", "Check if the image can be saved to a local device by a Save As function of the web browser."),
      "provenance_carrier": Q("iptc-photo-metadata-tests--social-2019", "are the embedded Exif and IPTC metadata (in the formats IIM and XMP) of the uploaded image still embedded?"),
      "relation_types": Q("iptc-photo-metadata-tests--social-2019", "Caption/description, Creator, Copyright Notice, Credit Line (= the 4Cs )"),
      "retention_results": Q("iptc-photo-metadata-tests--social-2019", "Embedded Creator replaced by account owner."),
      "retention_results_2": Q("iptc-photo-metadata-tests--social-2019", "No embedded metadata displayed, metadata is stripped off in SavedAs or downloaded files."),
      "retention_results_3": Q("iptc-photo-metadata-tests--social-2019", "SavedAs files have no XMP metadata."),
      "retention_results_4": Q("iptc-photo-metadata-tests--social-2019", "SaveAs files keep the embedded metadata."),
      "retention_results_5": Q("iptc-photo-metadata-tests--social-2019", "Passed through original file, preview can be SavedAs with stripped off metadata."),
      "finding": Q("iptc-photo-metadata-tests--research", "The results show that it is not impossible to preserve metadata in a workflow."),
    },
    relations=[{"rel": "has_part", "target": "iptc-metawatch"}, {"rel": "neighbour", "target": "c2pa-conformance"}],
    unchecked=["the 2016 and 2013 result tables", "the August 2014 software study", "the interoperability test procedures in detail"])

row(slug="iptc-metawatch", name="IPTC Metawatch", aka=["Metawatch"], url="https://metawatch.iptc.org/", operator="IPTC",
    lineage="media", kind="monitor", capability=["tests"],
    provenance_object="the lead photograph of a news article, as served to the reader",
    relation_types=["creation (creator)", "credit", "rights (copyright)", "description (caption)", "data-mining preference (PLUS Data Mining)", "C2PA Content Credentials"],
    provenance_carrier="embedded metadata (Exif, IPTC IIM and XMP) and C2PA manifests",
    unit="a news publisher, sampled each month through up to 20 recent articles",
    transformations_tested=["publication through a news site's pipeline (CMS, CDN, image optimisation)"],
    retention_results="October 2026: 7.2% of editorial images carried a credit or copyright notice (IMATAG's 2018 test: 8%); 321 of 425 crawlable publishers kept none of the scored IPTC fields; 27 of 6,580 images carried a C2PA manifest",
    cadence="monthly, on the first of each month (the first run dated 2026-06-03)", count={"value": "508 news publishers in 122 countries visited; 425 crawlable in the October run", "as_of": "2026-10"},
    data_access="every run published as open data", license="CC BY 4.0 (each run's data)",
    lifecycle={"state": "active", "detail": "measured monthly since June 2026 (first run 2026-06-03); introduced at the IPTC Photo Metadata Conference in early September 2026; announced 5 October 2026"}, founded="first run 2026-06-03; announced 5 October 2026",
    version_and_time={"first_run": "2026-06-03", "conference": "2026-09 (the post of 8 September: 'Last Thursday')", "announced": "2026-10-05", "run_reported": "October 2026", "read": "2026-10-29"},
    negative_tags=["NOT the 2019 IPTC social-media test: it measures news publishers monthly", "NOT a C2PA verifier"],
    evidence={
      "self_description": Q("iptc-metawatch--announcement", "a free, open monitor that checks every month whether more than 500 news publishers in 122 countries keep the credits, captions and rights information embedded in their photographs"),
      "count": Q("iptc-metawatch--announcement", "On the first of each month our well-behaved crawler visits 508 news publishers in 122 countries, takes up to 20 recent articles from each, and reads the lead photograph of every article."),
      "license": Q("iptc-metawatch--announcement", "every run is published as open data under CC BY 4.0"),
      "retention_results": Q("iptc-metawatch--announcement", "In 2018 IMATAG found that 8% of editorial images carried a credit or copyright notice. Applying the same test to our October run gives 7.2%."),
      "retention_results_2": Q("iptc-metawatch--announcement", "In the October run, 321 of the 425 publishers we could crawl, three out of four kept none of the IPTC fields we score on any image we sampled."),
      "transformations_tested": Q("iptc-metawatch--announcement", "Stripping appears to happen in the publishing pipeline, which means that publishers can fix it."),
      "c2pa": Q("iptc-metawatch--announcement", "Leaving out IPTC’s own site, 27 of the 6,580 images we analysed carried a C2PA manifest"),
      "lineage_note": Q("iptc-metawatch--announcement", "Metawatch builds on IMATAG’s 2018 State of Image Metadata study and IPTC’s own prototype crawler from 2019"),
      "access_limit": Q("iptc-metawatch--announcement", "AP and USA Today began blocking automated access this month. It is a reminder that bot-blocking aimed at AI also shuts out research."),
      "since_june": Q("iptc-metawatch--announcement", "Across the 294 publishers we have measured every month since June"),
      "first_run": {"src": "iptc-metawatch--overview", "basis": "observed", "quote": None, "note": "the chart labels of the saved overview page (SVG titles, stripped from its text), e.g. 'France: #1 of 26 on 2026-06-03'"},
      "conference": Q("iptc-metawatch--conference-post", "Lastly, Brendan Quinn appeared again to introduce Metawatch , IPTC’s new public service that monitors real-world usage of metadata in images across the global news industry, tracking IPTC/XMP, C2PA, AI opt-outs and more."),
      "conference_date": Q("iptc-metawatch--conference-post", "Last Thursday, the photo metadata industry came together for the 2026 IPTC Photo Metadata Conference."),
    },
    relations=[{"rel": "part_of", "target": "iptc-photo-metadata-tests"}, {"rel": "neighbour", "target": "c2pa-conformance"}],
    unchecked=["the published run data", "IMATAG's 2018 study", "the copyright share on the site (5.3% of 6,514 images) against the announcement's figure (5.6% of 6,580)"])

# ---------------------------------------------------------------- Nanopublications
row(slug="nanopublications", name="Nanopublications", aka=["nanopub", "Nanopub Registry", "Nanopub Query", "Nanodash"], url="https://nanopub.net/",
    operator="the nanopublication community (nanopub.net)", lineage="scholarly record", kind="publication model and service ecosystem",
    capability=["expresses", "records"],
    provenance_object="an assertion: a small knowledge-graph snippet published on its own",
    relation_types=["assertion provenance (how the assertion came to be)", "publication info (who created the nanopublication, when, licence)", "signature (signing at publication)"],
    provenance_carrier="RDF graphs: assertion, provenance and publication-info parts of one nanopublication",
    unit="a nanopublication",
    transformations_tested=[], retention_results="not tested: the model carries provenance; it does not measure its survival",
    data_access="decentralized publishing and SPARQL query services", lifecycle={"state": "active", "detail": "second-generation Registry and Query services; the legacy nanopub-server keeps old unsigned nanopublications"},
    version_and_time={"architecture_page_updated": "2026-10-28", "read": "2026-10-29"},
    negative_tags=["NOT a test of whether provenance survives reuse", "publication and signing do not settle an assertion's truth"],
    evidence={
      "self_description": Q("nanopublications--home", "A nanopublication is a small knowledge graph snippet with metadata that is treated as an independent (scientific) publication."),
      "relation_types": Q("nanopublications--home", "Provenance : This part describes how the assertion above came to be."),
      "relation_types_2": Q("nanopublications--home", "Publication Info : This part contains metadata about the nanopublication as a whole, such as when and by whom it was created and the license terms for its reuse."),
      "provenance_carrier": Q("nanopublications--home", "Nanopublications are implemented in the language RDF"),
      "lifecycle": Q("nanopublications--architecture", "The legacy nanopub-server ( instance , code ) is still used to keep the old (unsigned) nanopublications, but has otherwise no longer a function in the latest generation of the ecosystem."),
      "data_access": Q("nanopublications--architecture", "They allow for decentrally querying the published nanopublications via a number of SPARQL endpoints"),
      "signing": Q("nanopublications--architecture", "most importantly for signing and publishing, over HTTP"),
    },
    relations=[{"rel": "neighbour", "target": "provstore"}],
    unchecked=["the guidelines and the published articles", "record counts in the Registry (third-party accounts give 'millions')", "the nanopub Agent Skill", "the operator: nanopub.net names no organization; a third-party account names Knowledge Pixels as Nanodash's developer"])

# ---------------------------------------------------------------- C2PA
row(slug="c2pa-conformance", name="C2PA Conformance Program and Explorer", aka=["C2PA Conforming Products List", "Content Credentials conformance"],
    url="https://c2pa.org/conformance/", operator="Coalition for Content Provenance and Authenticity (C2PA), Conformance Task Force", lineage="media", kind="registry",
    capability=["expresses", "records"],
    provenance_object="a digital asset with its Content Credential (C2PA manifest); the registry's own unit is the product or signer",
    relation_types=["signing", "creation and edit history (ingredients)", "trust-list membership"],
    provenance_carrier="signed C2PA manifests; the conformance lists as JSON",
    unit="a conforming generator or validator product, or a trust-list entry",
    transformations_tested=[], retention_results="not tested here: conformance concerns producing and validating C2PA data correctly",
    count={"value": "286 records in the conforming-products JSON list", "as_of": "2026-10-29"},
    data_access="Conformance Explorer; JSON lists on GitHub", lifecycle={"state": "active", "detail": "program opened June 2025, now v0.2"}, founded="June 2025 (the program)",
    authority_dependencies=["C2PA Steering Committee", "C2PA Trust List", "C2PA TSA Trust List", "the Certificate Policy"],
    version_and_time={"program": "v0.2", "explainer_read": "2.4", "specification_latest": "2.5 (the saved Explainer's version menu)", "read": "2026-10-29"},
    negative_tags=["Content Credentials do not judge whether provenance data is 'true'", "NOT IPTC embedded metadata", "C2PA does not address human or organizational identity"],
    evidence={
      "self_description": Q("c2pa-conformance--conformance", "The C2PA Conformance Program provides assurance that products adhere to the Content Credentials specification, and fulfill a set of security requirements to ensure they are producing and validating C2PA data correctly."),
      "lifecycle": Q("c2pa-conformance--conformance", "After opening the program in June 2025, we have upgraded our conformance program to v0.2."),
      "unit": Q("c2pa-conformance--conformance", "Conforming products are placed on a publicly-accessible list."),
      "limit": Q("c2pa-conformance--explainer-2.4", "It is important to highlight that Content Credentials do not provide value judgments about whether a given set of provenance data is 'true', but instead merely whether the provenance information is well-formed and free from tampering, valid and trusted"),
      "limit_2": Q("c2pa-conformance--explainer-2.4", "provenance information alone cannot tell you whether the digital content is true, accurate or factual."),
      "identity": Q("c2pa-conformance--explainer-2.4", "The C2PA specification does not directly address the topic of human or organizational identity"),
      "ingredients": Q("c2pa-conformance--explainer-2.4", "the ingredient’s provenance cannot be verified in the same way as the provenance data of the asset in which it is contained."),
      "count": {"src": "c2pa-conformance--products-json", "basis": "observed", "quote": None, "note": "list length counted in the saved JSON"},
      "specification_latest": Q("c2pa-conformance--explainer-2.4", "C2PA Specifications 2.4 C2PA Specifications 2.5 2.4 2.3"),
    },
    relations=[{"rel": "neighbour", "target": "iptc-metawatch", "note": "Metawatch found 27 C2PA manifests in 6,580 news images, October 2026"}],
    unchecked=["the C2PA Trust List and TSA Trust List entries (components the program runs, in authority_dependencies)", "the Content Authenticity Initiative's tools"])

# ---------------------------------------------------------------- Data Provenance Initiative
row(slug="data-provenance-initiative", name="Data Provenance Initiative", aka=["Data Provenance Explorer", "Data Provenance Collection", "Data Provenance Card"],
    url="https://www.dataprovenance.org/", operator="the Data Provenance Initiative (a volunteer collective of AI researchers; the founding paper by Shayne Longpre and 16 other authors)", lineage="training data", kind="audit collection and measurement systems",
    capability=["records"],
    provenance_object="a fine-tuning dataset, traced through its collection to its sources",
    relation_types=["derivation (source and lineage)", "creators", "licences", "subsequent use"],
    provenance_carrier="audit metadata per dataset; a Data Provenance Card generated for a chosen subset",
    unit="a dataset within a collection",
    count={"value": "4,000+ datasets audited and 14,000 web domains tracked (the site, 2026-10-29); the first release audited 44 collections, 1800+ fine-tuning text-to-text datasets (the README)", "as_of": "2026-10-29"},
    transformations_tested=["dataset repackaging and hosting (licence carried or lost on hosting sites)"],
    retention_results="the founding paper reports licence omission of 70%+ and error rates of 50%+ on widely used hosting sites",
    data_access="repository scripts to filter and download; four public measurement systems on the site (the Data Provenance Explorer, the Web Consent Explorer, Open Model Evolution, the AI Observatory), their text in the site's script bundle",
    lifecycle={"state": "active", "detail": None}, founded="2023 (arXiv:2310.16787, v1 25 October 2023)",
    version_and_time={"paper_v1": "2023-10-25", "paper_v3": "2023-11-04", "read": "2026-10-29"},
    negative_tags=["NOT legal advice (its own notice)", "describing a collection does not establish which model used it", "initiative, explorer and collection are distinct records"],
    evidence={
      "self_description": Q("data-provenance-initiative--repo-readme", "The Data Provenance Initiative is a multi-disciplinary volunteer effort to improve transparency, documentation, and responsible use of training datasets for AI."),
      "count": Q("data-provenance-initiative--repo-readme", "Through a large scale audit of 44 data collections, spanning 1800+ finetuning text-to-text datasets"),
      "provenance_carrier": Q("data-provenance-initiative--repo-readme", "Generating a subset of data from this repository will create a `Data Provenance Card`---symbolic attribution for all constituent datasets"),
      "relation_types": Q("data-provenance-initiative--paper", "We develop tools and standards to trace the lineage of these datasets, from their source, creators, series of license conditions, properties, and subsequent use."),
      "retention_results": Q("data-provenance-initiative--paper", "We also observe frequent miscategorization of licenses on widely used dataset hosting sites, with license omission of 70%+ and error rates of 50%+."),
      "finding": Q("data-provenance-initiative--paper", "This points to a crisis in misattribution and informed use of the most popular datasets"),
      "negative": Q("data-provenance-initiative--repo-readme", "**This repository does NOT constitute legal advice.**"),
      "systems": Q("data-provenance-initiative--site-bundle", "Four public measurement systems"),
      "count_now": Q("data-provenance-initiative--site-bundle", "value:\"4,000+\",label:\"datasets audited\""),
      "collective": Q("data-provenance-initiative--site-bundle", "We are a volunteer collective of AI researchers conducting large-scale audits of the systems and resources that shape modern AI."),
      "scope_now": Q("data-provenance-initiative--site-bundle", "It now also covers web consent, open model markets, concentration of power, and how people use AI"),
    },
    relations=[{"rel": "sibling", "url": "https://www.machinemediation.org/aggregators/data-provenance-explorer/", "label": "its MMRS meta-aggregator record", "note": "the Initiative's explorer, one of its four systems, read for reception there; the Initiative and its explorer are distinct records"}],
    unchecked=["the four systems one by one", "the multimodal extension (arXiv:2412.17847) in full", "data licence of the audit"])

# ---------------------------------------------------------------- AttributionBench / AttriBench
row(slug="attributionbench", name="AttributionBench", aka=["AttributionBench (OSU)"], url="https://osu-nlp-group.github.io/AttributionBench/",
    operator="OSU NLP Group (The Ohio State University)", lineage="answer engines", kind="benchmark",
    capability=["tests"],
    provenance_object="a generated claim and the evidence it cites",
    relation_types=["support (is the claim fully supported by its cited evidence)"],
    provenance_carrier="citations in a generated answer",
    unit="a claim–evidence pair with a binary attribution label",
    transformations_tested=["generation with citations, from the constituent datasets' response sources (search-augmented models, dialogue systems, PaLM, WebGPT, GPT-3.5, Alpaca)"],
    retention_results="a fine-tuned GPT-3.5 reaches about 80% macro-F1 on the binary task (project abstract)",
    data_access="Hugging Face dataset", license="apache-2.0 (dataset card)", lifecycle={"state": "published", "detail": "arXiv:2402.15089; Findings of ACL 2024, pages 14919–14935"},
    negative_tags=["NOT AttriBench: it asks whether evidence supports a claim, not who wrote a quote", "evidence support is not credit to the original author"],
    evidence={
      "self_description": Q("attributionbench--project", "we present AttributionBench, a comprehensive benchmark compiled from various existing attribution datasets."),
      "relation_types": Q("attributionbench--project", "whether every claim within the generated responses is fully supported by its cited evidence"),
      "retention_results": Q("attributionbench--project", "even a fine-tuned GPT-3.5 only achieves around 80% macro-F1 under a binary classification formulation."),
      "license": Q("attributionbench--dataset-card", "license: apache-2.0"),
      "aggregation": Q("attributionbench--dataset-card", "We constructed this dataset from multiple existing data sources in a unified format"),
      "venue": Q("attributionbench--acl-anthology", "Findings of the Association for Computational Linguistics: ACL 2024"),
      "pages": Q("attributionbench--acl-anthology", "Pages: 14919–14935"),
      "error_shares": Q("attributionbench--project", "Over 66%"),
    },
    disambiguation=[{"neighbour": "attribench", "context": "quote attribution, author, suppression, Berman et al., 2026"}],
    relations=[{"rel": "neighbour", "target": "attribench"}],
    unchecked=["the seven constituent datasets one by one (ExpertQA, Stanford-GenSearch, AttributedQA, LFQA, BEGIN, HAGRID, AttrEval-GenSearch)"])

row(slug="attribench", name="AttriBench", aka=["Attribution Bias in Large Language Models"], url="https://huggingface.co/datasets/bermaneh/AttriBench",
    operator="Eliza Berman, Bella Chang, Daniel B. Neill, Emily Black", lineage="answer engines", kind="benchmark",
    capability=["tests"],
    provenance_object="a quote and its author",
    relation_types=["authorship (who wrote the quote)", "suppression (attribution omitted though authorship information is available)"],
    provenance_carrier="the model's answer naming, or not naming, an author",
    unit="a quote of 5–30 words with its canonical author",
    count={"value": "15,620 quotes from 6,292 unique authors across two splits", "as_of": "dataset card"},
    transformations_tested=["quote attribution by 11 widely used LLMs across prompt settings"],
    retention_results="large and systematic disparities in attribution accuracy between race, gender and intersectional groups; suppression widespread and unevenly distributed",
    license="CC BY 4.0", lifecycle={"state": "published", "detail": "accepted at COLM 2026"},
    version_and_time={"v1": "2026-04-06", "v2": "2026-09-24", "read": "2026-10-29"},
    negative_tags=["NOT OSU's AttributionBench", "NOT attribench, the 2023 PyTorch library for feature-attribution maps", "NOT AttriBench, Eureka Simulations' performance-attribution exercise", "fame is proxied by Google Search hit counts"],
    evidence={
      "self_description": Q("attribench--paper", "we introduce AttriBench, the first fame- and demographically-balanced quote attribution benchmark dataset."),
      "relation_types": Q("attribench--paper", "We further introduce and investigate suppression, a distinct failure mode in which models omit attribution entirely, even when the model has access to authorship information."),
      "retention_results": Q("attribench--paper", "We find that suppression is widespread and unevenly distributed across demographic groups"),
      "transformations_tested": Q("attribench--paper", "we evaluate 11 widely used LLMs across different prompt settings"),
      "count": Q("attribench--dataset-card", "**15,620 quotes** from **6,292 unique authors** across two splits"),
      "version_and_time": Q("attribench--paper", "[v1]\nMon, 6 Apr 2026 22:40:03 UTC (2,212 KB)"),
      "version_2": Q("attribench--paper", "[v2] Thu, 24 Sep 2026 19:36:19 UTC (3,003 KB)"),
      "lifecycle": Q("attribench--paper", "Accepted at COLM 2026. 25 pages"),
      "fame_proxy": Q("attribench--dataset-card", "Google Search hit count, used as a fame proxy."),
    },
    disambiguation=[{"neighbour": "attributionbench", "context": "claim support from cited evidence, OSU NLP Group, macro-F1"},
                    {"label": "attribench (PyPI)", "context": "PyTorch, feature attribution maps, XAI metrics, 2023 (the capture of 2026-10-29, cards 2 and 3)"},
                    {"label": "AttriBench (Eureka Simulations)", "context": "Brinson performance attribution, executive education (the capture of 2026-10-29, card 5)"}],
    relations=[{"rel": "neighbour", "target": "attributionbench"}],
    unchecked=["the paper's suppression definitions and prompts (full text)"])

# ---------------------------------------------------------------- ProvStore
row(slug="provstore", name="ProvStore", aka=["OpenProvenance ProvStore"], url="https://openprovenance.org/",
    operator="OpenProvenance (the PROV tool suite; the landing page © University of Sussex, 2024); maintainer Dong Huynh; ProvStore ran at the University of Southampton from 2013 and at King's College London from 2018", lineage="computational lineage", kind="repository (retired)",
    capability=["records"],
    provenance_object="a W3C PROV document",
    relation_types=["the PROV model: entities, activities, agents, derivations"],
    provenance_carrier="PROV documents (PROV-N, PROV-JSON, PROV-XML and others)",
    unit="a provenance document",
    transformations_tested=[], retention_results="not applicable",
    lifecycle={"state": "ended", "detail": "retired December 2024, per the maintainer's page updated 12 September 2026; the OpenProvenance landing page still says it is coming back soon"},
    version_and_time={"started": "2013 (University of Southampton)", "moved": "2018 (King's College London)", "retired": "2024-12", "maintainer_update": "2026-09-12", "landing_page_read": "2026-10-29"},
    negative_tags=["a live landing page is not a live repository", "NOT PROV Tokyo (a streetwear shop in Shibuya) or PROV Exam (licensing-exam study materials), both composed at the name on 2026-10-29"],
    evidence={
      "self_description": Q("provstore--openprovenance", "A provenance repository that allows storing, browsing, and managing provenance documents via a Web interface or a REST API."),
      "landing": Q("provstore--openprovenance", "ProvStore is coming back soon."),
      "lifecycle": Q("provstore--maintainer", "Updated 12-Sep-2026 : ProvStore was retired in December 2024."),
      "history": Q("provstore--maintainer-software", "It ran at the University of Southampton from 2013 and at King's College London from 2018, and was retired in December 2024."),
      "landing_owner": Q("provstore--openprovenance", "© University of Sussex, 2024."),
      "sibling_service": Q("provstore--openprovenance", "A RESTful web service that validates PROV descriptions against the PROV Constraints specification."),
    },
    relations=[{"rel": "neighbour", "target": "nanopublications", "note": "a reading: both carry provenance as published records (PROV documents; nanopublications' provenance graphs)"}],
    unchecked=["whether the public ProvStore documents were archived anywhere"])

# ---------------------------------------------------------------- WikiWho
row(slug="wikiwho", name="WikiWho", aka=[], url="https://wikiwho.wmcloud.org/",
    operator="first developed by Karlsruhe Institute of Technology and GESIS; since August 2021 maintained at Wikimedia, by Community Tech and the Wiki Education Foundation (the MediaWiki page's text) or Moderator Tools and the Wiki Education Foundation (its infobox)",
    lineage="authorship and reuse", kind="algorithm and API", capability=["records", "tests"],
    provenance_object="a single token (word) of a Wikipedia article",
    relation_types=["origin (the revision and editor that introduced the token)", "deletion", "reintroduction"],
    provenance_carrier="the article's full revision history, re-parsed",
    unit="a token in an article revision",
    transformations_tested=["every edit in an article's revision history"],
    retention_results="per token: when it entered, who wrote it, every removal and reinsertion; method evaluated at 95% on revision-rich articles",
    data_access="the WikiWho and WhoColor APIs", lifecycle={"state": "active", "detail": "moved to Wikimedia Cloud Services in August 2021; the GESIS host is to give way to Wikimedia"},
    version_and_time={"algorithm": "WWW 2014", "moved": "2021-08", "read": "2026-10-29"},
    evidence={
      "self_description": Q("wikiwho--api-readme", "The WikiWho API gives access to the provenance/changes of words (tokens) in Wikipedia articles."),
      "relation_types": Q("wikiwho--mediawiki", "find out who wrote and/or removed and/or reinserted which exact text at token level at what revision ."),
      "retention_results": Q("wikiwho--mediawiki", "The original algorithm working behind the scenes is described in a WWW 2014 paper , along with an extensive evaluation resulting in 95% accuracy on fairly revision-rich articles."),
      "operator": Q("wikiwho--mediawiki", "In August 2021, it was moved to Wikimedia Cloud Services infrastructure and is now maintained and under further development by Community Tech and the Wiki Education Foundation ."),
      "lifecycle": Q("wikiwho--api-readme", "In the future, only Wikimedia will continue its support."),
      "earlier_state": Q("wikiwho--meta-research", "We currently offer the service in English, German, Turkish and Basque, with more languages planned."),
      "precision_note": Q("wikiwho--meta-research", "the task of identifying the \"correct\" original author of a piece of text in a WP article is not trivial."),
      "operator_2": Q("wikiwho--mediawiki", "Group: Moderator Tools • Wiki Education Foundation"),
      "whocolor": Q("wikiwho--mediawiki", "This service can be thought of as an additional service on top of the core WikiWho data"),
      "wikis": {"src": "wikiwho--mediawiki", "basis": "observed", "quote": None, "note": "the 'Currently supported wikis' section of the saved page lists 71 entries, 70 distinct (Swedish twice)"},
    },
    count={"value": "70 supported wikis", "as_of": "the MediaWiki page, read 2026-10-29"},
    relations=[{"rel": "has_part", "label": "WhoColor", "note": "a service on top of WikiWho's data"}, {"rel": "has_part", "label": "Who Wrote That?", "note": "a browser extension powered by the WhoColor API"}],
    negative_tags=["the Meta research page still describes a beta for four languages: an earlier state of the project", "NOT wikiHow, the how-to site, composed in its place at the name on 2026-10-29"],
    unchecked=["the WWW 2014 paper itself"])

# ---------------------------------------------------------------- MMM and SDBM
row(slug="mapping-manuscript-migrations", name="Mapping Manuscript Migrations", aka=["MMM", "MMM Semantic Portal"], url="https://mappingmanuscriptmigrations.org/",
    operator="University of Oxford, University of Pennsylvania (Schoenberg Institute for Manuscript Studies), IRHT-CNRS, Aalto University", lineage="manuscripts and books", kind="aggregator (linked open data)",
    capability=["records"],
    provenance_object="a medieval or Renaissance manuscript and the events of its history",
    relation_types=["ownership", "sale and transfer events", "place", "works contained"],
    provenance_carrier="RDF mapped to a unified model drawing on CIDOC CRM and FRBRoo",
    unit="a manuscript, reconciled across three source databases",
    count={"value": "217,700 manuscripts and other entities in the portal; 262,000 source records combined", "as_of": "the white paper"},
    data_access="SPARQL endpoint on Linked Data Finland; a Sampo-UI semantic portal; a copy on Zenodo", license="CC BY-NC 4.0 (the MMM data)",
    lifecycle={"state": "project ended", "detail": "funded 2017–2020 by the Digging into Data Challenge; the portal home is a JavaScript application, unreadable to a plain fetch"},
    founded="2017 (funding period 2017–2020)",
    version_and_time={"project": "2017–2020", "read": "2026-10-29"},
    negative_tags=["NOT the Schoenberg Database itself: it aggregates SDBM with Bibale and the Bodleian's catalogue"],
    evidence={
      "self_description": Q("mapping-manuscript-migrations--white-paper", "Its main goal is to combine data from several disparate sources about medieval and Renaissance manuscripts, and to use the aggregated data to explore a range of research questions about their history and provenance."),
      "sources": Q("mapping-manuscript-migrations--white-paper", "The project took the data from three existing databases (the Schoenberg Database of Manuscripts, Medieval Manuscripts in Oxford Libraries, and Bibale) and turned them into Linked Open Data (LOD)."),
      "count": Q("mapping-manuscript-migrations--white-paper", "the 217,700 manuscripts and other entities can be searched, browsed, and analyzed"),
      "license": Q("mapping-manuscript-migrations--white-paper", "The MMM data are made available for reuse under a CC BY-NC 4.0 license"),
      "units_compared": Q("mapping-manuscript-migrations--white-paper", "The former takes a single manuscript as the basic unit, and attaches the evidence of its history to that record."),
      "lifecycle": Q("mapping-manuscript-migrations--white-paper", "is a project funded between 2017 and 2020 by the Digging into Data Challenge."),
      "data_access": Q("mapping-manuscript-migrations--white-paper", "A copy of the dataset was published through the Zenodo repository."),
    },
    relations=[{"rel": "has_part", "target": "schoenberg-database", "note": "the SDBM is one of the three source databases (evidence: sources)"}],
    unchecked=["the live portal (JavaScript)", "the Zenodo copy and its record", "Bibale's present state", "whether the data are maintained after the project's end"])

row(slug="schoenberg-database", name="Schoenberg Database of Manuscripts", aka=["SDBM"], url="https://sdbm.library.upenn.edu/",
    operator="Schoenberg Institute for Manuscript Studies, University of Pennsylvania", lineage="manuscripts and books", kind="database",
    capability=["records"],
    provenance_object="an observation of a pre-modern manuscript in a catalogue, inventory or other source",
    relation_types=["sale", "location", "ownership"],
    provenance_carrier="observation records with a VIAF-based name authority",
    unit="an observation (an entry in a source that documents a manuscript)",
    count={"value": "over 14,000 auction and sales catalogs, inventories and other sources (home page); 240,000 records (MMM white paper, 2020); the home page's source-type facet sums to over 259,000 entries for its top three types alone", "as_of": "2026-10-29 (home page); white paper"},
    intake="continuous; registered users contribute observations and batch uploads",
    data_access="search, download, SPARQL endpoint", license="CC BY-SA 4.0 for downloaded search results",
    lifecycle={"state": "active", "detail": None},
    evidence={
      "self_description": Q("schoenberg-database--home", "The SDBM continuously aggregates and updates historic observations of pre-modern manuscripts drawn from over 14,000 auction and sales catalogs, inventories, catalogs from institutional and private collections, and other sources that document the sales and locations of these books from around the world."),
      "license": Q("schoenberg-database--home", "Download Search Results for your own use under a Creative Commons Attribution-ShareAlike 4.0 Unported License"),
      "unit": Q("mapping-manuscript-migrations--white-paper", "The latter focuses on an “observation” of a manuscript in a sales or auction catalogue or collection catalogue"),
      "count": Q("mapping-manuscript-migrations--white-paper", "Schoenberg Database of Manuscripts (Schoenberg Institute for Manuscript Studies, 240,000 records)"),
    },
    relations=[{"rel": "part_of", "target": "mapping-manuscript-migrations"}],
    unchecked=["the database's own current total of entries", "whether the white paper's figures are the operator's (the MMM team includes the Institute's staff)"])

# ---------------------------------------------------------------- VroniPlag
row(slug="vroniplag-wiki", name="VroniPlag Wiki", aka=["VroniPlag"], url="https://vroniplag.fandom.com/de",
    operator="a volunteer wiki on Fandom (formerly Wikia); German Wikipedia's infobox names Martin Heidingsfelder as founder, and its text says he started it by his own account, a claim the project disputes", lineage="authorship and reuse", kind="documentation wiki",
    capability=["records", "tests"],
    transformations_tested=["the reuse of source text in a thesis, documented fragment by fragment and checked by a second person"],
    provenance_object="a passage of a doctoral thesis and the source it reproduces without attribution",
    relation_types=["unattributed reuse (plagiarism fragment)", "source text"],
    provenance_carrier="text-parallel documentation: page-by-page fragments, each classified and checked by a second person",
    unit="a thesis, documented as fragments",
    count={"value": "201 dissertations and 13 habilitation theses named (German Wikipedia, as of 3 April 2023); at least 90 doctorates revoked after a documentation (as of 30 April 2024)", "as_of": "2023-04-03 / 2024-04-30"},
    retention_results="the share of a thesis's pages found to contain plagiarism, per thesis",
    lifecycle={"state": "active", "detail": "online since 28 March 2011; the wiki returned 403 to a plain fetch on 2026-10-29, so its own figures were not read"},
    founded="28 March 2011", license="CC BY-SA 3.0 (English Wikipedia's infobox)",
    negative_tags=["NOT GuttenPlag Wiki, from which it grew", "publishes a case only where serious plagiarism was found, after notifying the university"],
    evidence={
      "self_description": Q("vroniplag-wiki--wikipedia", "is a [[wiki]] started 28 March 2011 at [[Wikia]] that examines and documents the extent of [[plagiarism]] in German doctoral [[theses]].", basis="third-party"),
      "method": Q("vroniplag-wiki--wikipedia", "Each fragment is classified as to the kind of plagiarism and must be verified by a second person before it is acceptable.", basis="third-party"),
      "policy": Q("vroniplag-wiki--wikipedia", "Before publication, the office of academic integrity at the university in question is formally notified, as any revocation of title must be done by the university.", basis="third-party"),
      "count": Q("vroniplag-wiki--dewiki", "erhöhte sich die Zahl der namentlich genannten untersuchten Arbeiten auf 201 Dissertationen und 13 [[Habilitationsschrift]]en", basis="third-party"),
      "consequence": Q("vroniplag-wiki--dewiki", "mindestens 90 Personen im Nachgang einer Dokumentation auf ''VroniPlag Wiki'' der Doktorgrad", basis="third-party"),
      "founder": Q("vroniplag-wiki--dewiki", "| Gründer         = [[Martin Heidingsfelder]]", basis="third-party"),
      "founder_text": Q("vroniplag-wiki--dewiki", "nach eigenen Angaben durch [[Martin Heidingsfelder]] unter dem [[Pseudonym]] „Goalgetter“", basis="third-party"),
    },
    relations=[],
    unchecked=["the wiki's own case list and statistics (403 on a plain fetch; its overview card read 'Es dokumentiert 204 Disse…' on 2026-10-29)", "the current licence on Fandom"])

# ---------------------------------------------------------------- Getty
row(slug="getty-provenance-index", name="Getty Provenance Index", aka=["GPI", "Getty Provenance Index®"], url="https://www.getty.edu/databases-tools-and-technologies/provenance/",
    operator="Getty Research Institute (J. Paul Getty Trust)", lineage="objects and art", kind="database (linked open data)",
    capability=["records"],
    provenance_object="a work of art and the documents of its ownership and sale",
    relation_types=["ownership", "sale", "dealer stock", "inventory", "payment to artists"],
    provenance_carrier="transcribed primary documents: archival inventories, auction and dealer sales catalogs, dealer stock books",
    unit="a resource drawn from a primary document",
    count={"value": "over 12 million digitized, open-access resources", "as_of": "2026-10-29"},
    data_access="the Remodeled Index (Arches, linked open data), SPARQL queries in the Getty LOD Gateway, CSV exports on GitHub, and the Legacy Index during the transition",
    lifecycle={"state": "active", "detail": "transitioning to linked open data; archival inventories to follow"},
    founded="1974 by Burton Fredericksen (home page); the initiative page places its beginning in the early 1980s, gives 'Years 1981 – present', and calls it one of the GRI's foundational initiatives of the 1980s",
    version_and_time={"digital": "1984", "cd_rom": "1994", "online": "1998", "read": "2026-10-29"},
    negative_tags=["coverage varies by region, period and type of document"],
    evidence={
      "self_description": Q("getty-provenance-index--home", "The Getty Provenance Index® (GPI) contains over 12 million digitized, open-access resources that trace the origins, movements, and lineages of art and cultural artifacts."),
      "founded": Q("getty-provenance-index--home", "Founded in 1974 by Burton Fredericksen"),
      "founded_2": Q("getty-provenance-index--initiative", "The GPI began as an initiative within the Getty Museum’s Paintings department in the early 1980s led by curator Burton B. Fredericksen."),
      "lifecycle": Q("getty-provenance-index--home", "Archival Inventory data will also transition to this new format soon. While the Index transitions, the original datasets will remain accessible in the Legacy Index platform."),
      "version_and_time": Q("getty-provenance-index--home", "First compiled digitally in 1984, published on CD-ROM in 1994, and launched online in 1998"),
      "coverage": Q("getty-provenance-index--whats-covered", "The quantity and scope of research material available in the Getty Provenance Index® varies by region, period, and type of document."),
      "units": {"src": "getty-provenance-index--whats-covered", "basis": "operator", "quote": "The Provenance Index encompasses over 12 million resources extracted from more than 22,000 catalogs", "note": "said in the page's Sales Catalogs section; the 12 million of the whole Index is the home page's (self_description)"},
      "founded_3": Q("getty-provenance-index--initiative", "Years 1981 – present"),
      "founded_4": Q("getty-provenance-index--initiative", "Established as one of the GRI’s foundational initiatives in the 1980s"),
      "stock_books": Q("getty-provenance-index--whats-covered", "more than 190,000 resources from the 15 stock books of Goupil & Cie./Boussod, Valadon & Cie in Paris (1846–1919)"),
      "data_access": Q("getty-provenance-index--home", "Query Getty Provenance Index data using SPARQL in the Getty LOD Gateway"),
    },
    relations=[],
    unchecked=["the data licence of the Remodeled Index", "the Public Collections and Collectors Files databases in detail"])

# ---------------------------------------------------------------- OLMoTrace
row(slug="olmotrace", name="OLMoTrace", aka=[], url="https://playground.allenai.org",
    operator="Allen Institute for AI (Ai2), with the University of Washington, UC Berkeley and Stanford", lineage="training data", kind="tracing tool",
    capability=["records"],
    provenance_object="a span of a language model's output and the training documents that contain it verbatim",
    relation_types=["verbatim match between output and training text"],
    provenance_carrier="the model's full training corpus, indexed with an extended infini-gram",
    unit="a span of model output matching training text verbatim (maximal spans, filtered by unigram probability and merged for display)",
    count={"value": "3.2 billion documents and 4.6 trillion tokens (OLMo-2-32B-Instruct's training data)", "as_of": "the paper, v2"},
    transformations_tested=["model generation, traced back to training text"],
    retention_results="returns matching documents within a few seconds; the authors state the matches are not causal and not citations",
    data_access="Ai2 Playground; the core open-sourced under the Apache 2.0 license", lifecycle={"state": "active", "detail": "ACL 2025 demo track"},
    version_and_time={"v1": "2025-04-09", "v2": "2025-07-08", "read": "2026-10-29"},
    negative_tags=["the retrieved documents are not causes of the output", "NOT a citation system", "traces a model only where the service provider has access to its full training data"],
    evidence={
      "self_description": Q("olmotrace--abs", "We present OLMoTrace, the first system that traces the outputs of language models back to their full, multi-trillion-token training data in real time."),
      "relation_types": Q("olmotrace--abs", "OLMoTrace finds and shows verbatim matches between segments of language model output and documents in the training text corpora."),
      "limit": Q("olmotrace--paper", "The retrieved documents should not be interpreted as having a causal effect on the LM output, or as supporting evidence or citations for the LM output."),
      "count": Q("olmotrace--paper", "which totals 3.2 billion documents and 4.6 trillion (Llama-2) tokens"),
      "data_access": Q("olmotrace--abs", "OLMoTrace is publicly available and fully open-source."),
      "license": Q("olmotrace--paper", "The core part of the system is open-sourced under the Apache 2.0 license."),
      "condition": Q("olmotrace--paper", "OLMoTrace can be applied to any LM as long as the service provider has access to its full training data"),
    },
    relations=[{"rel": "neighbour", "target": "data-provenance-initiative"}],
    unchecked=["the Playground itself", "infini-gram as a separate record"])

# ---------------------------------------------------------------- write
def norm(s): return re.sub(r"\s+", " ", s).strip()
problems = []
for r in ROWS:
    srcs = {}
    for f, ev in r["evidence"].items():
        sid = ev["src"]
        assert sid in MAN, (r["slug"], sid)
        srcs[sid] = {"url": MAN[sid]["url"], "read": MAN[sid]["fetched"][:10], "sha256": MAN[sid]["sha256"], "http": MAN[sid]["http"]}
        if ev.get("quote"):
            txt = norm((HERE / "sources" / f"{sid}.txt").read_text(encoding="utf-8"))
            if norm(ev["quote"]) not in txt:
                problems.append((r["slug"], f, sid, ev["quote"][:80]))
    r["sources"] = srcs
    r.setdefault("observed", {"on": "2026-10-29", "fetch": "read"})
out = {"name": "Provenance meta-aggregator census", "compiled": "2026-10-29", "schema_version": "1.0",
       "schema_note": "MMRS census fields extended for provenance: lineage, capability (expresses / records / tests), provenance_object, relation_types, provenance_carrier, transformations_tested, retention_results, authority_dependencies, version_and_time. Every quote is verbatim from a saved source (sources/manifest.json). Untested capability reads 'not tested'.",
       "organizing_question": "What provenance does this system carry, through which operation, on whose assertion, with what evidence of survival?",
       "rows": ROWS}
json.dump(out, open(HERE / "census.json", "w"), ensure_ascii=False, indent=1)
print(len(ROWS), "rows;", sum(len(r["evidence"]) for r in ROWS), "evidence items;", len(problems), "quote problems")
for p in problems: print("  ", p)
