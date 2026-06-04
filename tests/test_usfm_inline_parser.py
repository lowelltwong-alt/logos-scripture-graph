from pipelines.ingest.usfm_inline_parser import InlineContext, InlineParser


def test_word_tag_becomes_clean_text_and_word_token():
    result = InlineParser().parse(
        r'\w In|strong="H8064"\w* the beginning',
        InlineContext(passage_id="scripture:Gen.1.1", osis_ref="Gen.1.1"),
    )

    assert result.clean_text == "In the beginning"
    assert len(result.word_tokens) == 1
    token = result.word_tokens[0]
    assert token["surface_text"] == "In"
    assert token["strong"] == "H8064"
    assert token["source_marker"] == r'\w In|strong="H8064"\w*'


def test_nested_wj_plus_w_preserves_nesting_context():
    result = InlineParser().parse(
        r'\wj \+w Jesus|strong="G2424"\+w* said\wj*',
        InlineContext(passage_id="scripture:John.3.16", osis_ref="John.3.16"),
    )

    assert result.clean_text == "Jesus said"
    assert result.word_tokens[0]["surface_text"] == "Jesus"
    assert result.word_tokens[0]["strong"] == "G2424"
    assert result.word_tokens[0]["is_nested"] is True
    assert result.word_tokens[0]["nesting_context"] == ["wj"]


def test_footnote_with_hebrew_span_and_alternate_reading_is_sidecar_only():
    result = InlineParser().parse(
        r'Text\f + \fr 1:1 \ft Hebrew term \+wh אֱלֹהִ֑ים\+wh* here. \fqa alternate reading\f* after',
        InlineContext(passage_id="scripture:Gen.1.1", osis_ref="Gen.1.1"),
    )

    assert result.clean_text == "Text after"
    assert len(result.footnotes) == 1
    footnote = result.footnotes[0]
    assert footnote["reference"] == "1:1"
    assert "אֱלֹהִ֑ים" in footnote["text"]
    assert footnote["hebrew_word_spans"] == ["אֱלֹהִ֑ים"]
    assert footnote["alternate_readings"] == ["alternate reading"]
    assert r"\f " in footnote["raw_marker"]


def test_editorial_crossref_preserves_origin_target_and_candidate_osis():
    result = InlineParser().parse(
        r'child\x + \xo 1:23 \xt Isaiah 7:14\x* text',
        InlineContext(passage_id="scripture:Matt.1.23", osis_ref="Matt.1.23"),
    )

    assert result.clean_text == "child text"
    assert len(result.crossrefs) == 1
    crossref = result.crossrefs[0]
    assert crossref["origin"] == "1:23"
    assert crossref["target_text"] == "Isaiah 7:14"
    assert crossref["candidate_osis_refs"] == ["Isa.7.14"]
    assert crossref["relation_type"] == "editorial_cross_reference"
