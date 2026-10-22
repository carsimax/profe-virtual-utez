"""Presets, page sizes, callout palette and localized labels (ported from docgen.mjs)."""

# Preset APA 7 is the only exception to the house layout (1.5 cm margins, 9-11 pt, single spacing).
# Colors without '#'. Sizes in half-points (22 = 11 pt).
PRESETS = {
    "utez": dict(
        label="UTEZ institucional", font="Arial", fontHead="Arial", mono="Consolas",
        text="1B2633", muted="5B6573", head="002E60", accent="00735B", brand="009475", brand2="002E60",
        rule="009475", tableHead="002E60", tableHeadText="FFFFFF", band="EEF3F0", line="C9D3CD", labelFill="E6EFEA",
        size=20, h1=22, h2=21, h3=20, title=22, lineSpacing=240, after=100, firstLine=0, justify=False,
        margins=850, headingCase="normal", headNumbered=False, captionStyle="standard", tableStyle="banded",
        small=18, cell=20, lead=20, subtitle=20, cellLine=240, kvLine=240, titleLine=240, hdr=18, hdrDist=425,
        series=["009475", "2A78D6", "EB6834", "6250D6"]),
    "apa": dict(
        label="Académico APA 7", font="Times New Roman", fontHead="Times New Roman", mono="Courier New",
        text="000000", muted="404040", head="000000", accent="000000", brand="000000", brand2="000000",
        rule="000000", tableHead="FFFFFF", tableHeadText="000000", band="FFFFFF", line="000000", labelFill="F2F2F2",
        size=24, h1=24, h2=24, h3=24, title=24, lineSpacing=480, after=0, firstLine=720, justify=False,
        margins=1440, headingCase="apa", headNumbered=False, captionStyle="apa", tableStyle="apa",
        small=20, cell=22, lead=28, subtitle=30, cellLine=252, kvLine=264, titleLine=252, hdr=24, hdrDist=708,
        series=["1F4E79", "9E3508", "0A6155", "6250D6"]),
    "corporativo": dict(
        label="Corporativo", font="Calibri", fontHead="Calibri", mono="Consolas",
        text="262626", muted="595959", head="1F3864", accent="2E75B6", brand="1F3864", brand2="2E75B6",
        rule="2E75B6", tableHead="1F3864", tableHeadText="FFFFFF", band="F2F5FA", line="BFC9D9", labelFill="E8EEF7",
        size=20, h1=22, h2=21, h3=20, title=22, lineSpacing=240, after=100, firstLine=0, justify=False,
        margins=850, headingCase="normal", headNumbered=False, captionStyle="standard", tableStyle="banded",
        small=18, cell=20, lead=20, subtitle=20, cellLine=240, kvLine=240, titleLine=240, hdr=18, hdrDist=425,
        series=["2A78D6", "EB6834", "1BAF7A", "6250D6"]),
    "tecnico": dict(
        label="Técnico / software", font="Calibri", fontHead="Calibri", mono="Consolas",
        text="1F2328", muted="57606A", head="0B3D6E", accent="0B5CAD", brand="0B5CAD", brand2="C2410C",
        rule="0B5CAD", tableHead="0B3D6E", tableHeadText="FFFFFF", band="F3F6F9", line="C8D1DC", labelFill="E7EEF6",
        size=20, h1=22, h2=21, h3=20, title=22, lineSpacing=240, after=100, firstLine=0, justify=False,
        margins=850, headingCase="normal", headNumbered=True, captionStyle="standard", tableStyle="lines",
        small=18, cell=20, lead=20, subtitle=20, cellLine=240, kvLine=240, titleLine=240, hdr=18, hdrDist=425,
        series=["0B5CAD", "D95926", "1BAF7A", "9085E9"]),
    "editorial": dict(
        label="Editorial / ensayo", font="Georgia", fontHead="Georgia", mono="Consolas",
        text="1A1A1A", muted="55504A", head="1A1A1A", accent="8B1E3F", brand="8B1E3F", brand2="1F4E79",
        rule="8B1E3F", tableHead="FFFFFF", tableHeadText="1A1A1A", band="F7F4EF", line="1A1A1A", labelFill="F1EDE5",
        size=20, h1=22, h2=21, h3=20, title=22, lineSpacing=240, after=100, firstLine=0, justify=False,
        margins=850, headingCase="normal", headNumbered=False, captionStyle="standard", tableStyle="lines",
        small=18, cell=20, lead=20, subtitle=20, cellLine=240, kvLine=240, titleLine=240, hdr=18, hdrDist=425,
        series=["8B1E3F", "2A78D6", "008300", "EDA100"]),
}

PAGES = {"letter": dict(width=12240, height=15840), "a4": dict(width=11906, height=16838)}

# kind -> (fill, bar color, default title)
CALLOUTS = {
    "info": ("E8F1FB", "2563A8", "Nota"), "tip": ("E6F4EF", "00875F", "Sugerencia"),
    "warn": ("FFF4E5", "B86E00", "Atención"), "important": ("FDECEC", "B42318", "Importante"),
    "example": ("F3F0FA", "6250D6", "Ejemplo"),
}

L10N = {
    "es": dict(toc="Índice", lof="Índice de figuras", lot="Índice de tablas", fig="Figura", tab="Tabla",
               page="Página", of="de", refs="Referencias", source="Fuente", name="Nombre", group="Grupo",
               date="Fecha", score="Calificación", points="pts", answer="Respuesta", key="Clave de respuestas",
               correct="correcta", true="Verdadero", false="Falso", course="Asignatura", teacher="Docente"),
    "en": dict(toc="Contents", lof="List of Figures", lot="List of Tables", fig="Figure", tab="Table",
               page="Page", of="of", refs="References", source="Source", name="Name", group="Group",
               date="Date", score="Score", points="pts", answer="Answer", key="Answer key", correct="correct",
               true="True", false="False", course="Course", teacher="Teacher"),
}
