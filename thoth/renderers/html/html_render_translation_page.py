# standard library imports

# third party imports

# own imports
from thoth.model.norm.conformity import Conformity
from thoth.model.norm.driver import Driver
from thoth.model.norm.indicator import Indicator
from thoth.model.norm.multi_lingual_text import MultiLingualText
from thoth.model.norm.norm import Norm
from thoth.model.norm.reference import Reference


def render_list(multi_lingual_list: list[MultiLingualText], language: str) -> str:
    return f"""
<ul>
  {
    "\n  ".join(
        f"<li>{multi_lingual_text[language]}</li>" for multi_lingual_text in multi_lingual_list
    )
  }
</ul>
    """.strip()  # fmt: skip


def render_driver(driver: Driver, _language: str) -> str:
    return f"""
<!-- driver {driver.name} -->
    <div class="sub-part-title">
      {driver.name}
    </div>
    <table class="driver-table">
      {
        ""
        if driver.details is None
        else "\n      ".join(
            f'''
            <tr>
              <td/>
              <td>{detail}</td>
            </tr>
            '''.strip()
            for detail in driver.details
        )
      }
    </table>
<!-- driver {driver.name} -->
    """.strip()  # fmt: skip


def render_drivers(drivers: list[Driver], language: str) -> str:
    width = 100 // len(drivers)
    return f"""
<div class="sub-part">
  <table width="100%">
    <tr>
      <td width="*">
        {
          f'''</td>\n<td width="{width}%">'''.join(
              render_driver(driver, language) for driver in drivers
          )
        }
      </td>
    </tr>
  </table>
</div>
    """.strip()  # fmt: skip


def render_conformity(
    indicator: Indicator,
    conformity: Conformity,
    language_1: str,
    language_2: str,
) -> str:
    style = '"margin-left: 48px;"'
    return f"""
<!-- conformity {conformity.identifier} -->
  <tr>
    <td width="50%">
      <div class="sub-part">
        <div class="sub-sub-part">
          {indicator.identifier}/{conformity.identifier}
        </div>
      </div>
    </td>
    <td width="*">
      <div class="sub-part">
        <div class="sub-sub-part">
          {indicator.identifier}/{conformity.identifier}
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <div class="sub-part">
        <div class="sub-sub-part" style={style}>
         {conformity.description[language_1]}
        </div>
      </div>
    </td>
    <td width="*">
      <div class="sub-part">
        <div class="sub-sub-part" style={style}>
          {conformity.description[language_2]}
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <div class="sub-part">
        <div class="sub-sub-part" style={style}>
          {"" if conformity.guidance is None else f'''<em>{conformity.guidance[language_1]}</em>'''}
        </div>
      </div>
    </td>
    <td width="*">
      <div class="sub-part">
        <div class="sub-sub-part" style={style}>
          {"" if conformity.guidance is None else f'''<em>{conformity.guidance[language_2]}</em>'''}
        </div>
      </div>
    </td>
  </tr>
<!-- conformity {conformity.identifier} -->
    """.strip()


def render_indicator(indicator: Indicator, language_1: str, language_2: str) -> str:
    return f"""
<!-- indicator {indicator.identifier} -->
  <tr>
    <td width="50%">
      <div class="sub-part">
        <div class="indicator-title">
          {indicator.identifier} {indicator.title[language_1]}
        </div>
      </div>
    </td>
    <td width="*">
      <div class="sub-part">
        <div class="indicator-title">
          {indicator.identifier} {indicator.title[language_2]}
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <div class="sub-part">
        <div>
          {indicator.description[language_1]}
        </div>
      </div>
    </td>
    <td width="*">
      <div class="sub-part">
        <div>
          {indicator.description[language_2]}
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <div class="sub-part">
        <div class="sub-sub-part">
          <div class="sub-sub-part-title">
            Conformity indicators
          </div>
        </div>
      </div>
    </td>
    <td width="*">
      <div class="sub-part">
        <div class="sub-sub-part">
          <div class="sub-sub-part-title">
            Conformity indicators
          </div>
        </div>
      </div>
    </td>
  </tr>
  {"\n".join(render_conformity(indicator, conformity, language_1, language_2) for conformity in indicator.conformities)}
  <tr>
    <td width="50%">
      <div class="sub-part">
        <div class="sub-sub-part">
          <div class="sub-sub-part-title">
            Explanation
          </div>
        </div>
      </div>
    </td>
    <td width="*">
      <div class="sub-part">
        <div class="sub-sub-part">
          <div class="sub-sub-part-title">
            Explanation
          </div>
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <div class="sub-part">
        <div class="sub-sub-part">
        <div class="sub-sub-part">
          <div>
            {indicator.explanation[language_1]}
          </div>
        </div>
      </div>
    </td>
    <td width="*">
      <div class="sub-part">
        <div class="sub-sub-part">
        <div class="sub-sub-part">
          <div>
            {indicator.explanation[language_2]}
          </div>
        </div>
      </div>
    </td>
  </tr>
<!-- indicator {indicator.identifier} -->
    """.strip()


def render_reference(reference: Reference, language: str) -> str:
    return f"""
<!-- reference {reference.name} -->
  <div class="sub-part">
    <div class="reference">
      {reference.name}{
        "" if reference.url is None else f''' - <a href="{reference.url}">{reference.url}</a>'''
      }
    </div>
    {"" if reference.notes is None else render_list(reference.notes, language)}
  </div>
<!-- reference {reference.name} -->
    """.strip()  # fmt: skip


def render_translation(norm: Norm, language_1: str, language_2: str) -> str:
    return f"""
<html>
  <head>
    <!-- standard elements -->
    <style>
      table {{
        border-collapse: collapse;
        border-spacing: 0px 6px;
        margin: 24px 0px;
      }}
      th, td {{
        vertical-align: top;
        padding: 4px;
      }}
      ul {{
        list-style-type: "- ";
      }}
    </style>
    <!-- custom classes -->
    <style>
      .driver-table {{
        margin: 6px;
      }}
      .blue-box {{
        background-color: #DDE8F6;
        margin: -1px;
        padding: 1px;
      }}
      .norm-title {{
        margin: 12px 0px;
        padding: 4px 6px;
        font-weight: bold;
        font-size: larger;
        color: white;
        background-color: #325899;
      }}
      .norm-intro {{
        font-style: italic;
      }}
      .part {{
        margin: 0px 6px;
      }}
      .part-title {{
        margin: 6px 0px;
        font-weight: bold;
        font-size: larger;
      }}
      .sub-part {{
        margin: 8px 6px;
      }}
      .sub-part-title {{
        margin: 6px 0px;
        font-weight: bold;
        font-size: medium;
      }}
      .sub-sub-part {{
        margin: 4px 0px;
      }}
      .sub-sub-part-title {{
        margin: 6px 0px;
        font-weight: bold;
        font-size: medium;
        color: #2E5E7E;
      }}
      .indicator-title {{
        padding: 4px 6px;
        margin: 6px 0px;
        color: white;
        background-color: #325899;
      }}
      .reference {{
      }}
    </style>
  </head>
  <body>
    <!-- introduction -->
    <table width="100%">
      <tr>
        <td width="50%">
          <h1>{norm.identifier} - {norm.title[language_1]}</h1>
        </td>
        <td width="*">
          <h1>{norm.identifier} - {norm.title[language_2]}</h1>
        </td>
      </tr>
      <tr>
        <td width="50%">
          <div class="norm-intro">{norm.intro[language_1]}</div>
        </td>
        <td width="*">
          <div class="norm-intro">{norm.intro[language_2]}</div>
        </td>
      </tr>
    </table>
    <!-- detailed norm -->
    <table width="100%">
      <tr>
        <td width="50%">
          <div class="norm-title">
            {norm.identifier} - {norm.title[language_1]}
          </div>
        </td>
        <td width="*">
          <div class="norm-title">
            {norm.identifier} - {norm.title[language_2]}
          </div>
        </td>
      </tr>
      <tr>
        <td width="50%">
          <div class="part">
            <div class="part-title">
              <p>scope</p>
            </div>
            {norm.scope[language_1]}
          </div>
        </td>
        <td width="*">
          <div class="part">
            <div class="part-title">
              <p>scope</p>
            </div>
            {norm.scope[language_2]}
          </div>
        </td>
      </tr>
      <tr>
        <td width="50%">
          <div class="part">
            <div class="part-title">
              <p>triggers</p>
            </div>
            {render_list(norm.triggers, language_1)}
          </div>
        </td>
        <td width="*">
          <div class="part">
            <div class="part-title">
              <p>triggers</p>
            </div>
            {render_list(norm.triggers, language_2)}
          </div>
        </td>
      </tr>
      <tr>
        <td width="50%">
          <div class="blue-box">
            <div class="part">
              <div class="part-title">
                <p>criteria</p>
              </div>
              {render_list(norm.criteria, language_1)}
            </div>
          </div>
        </td>
        <td width="*">
          <div class="blue-box">
            <div class="part">
              <div class="part-title">
                <p>criteria</p>
              </div>
              {render_list(norm.criteria, language_2)}
            </div>
          </div>
        </td>
      </tr>
      <tr>
        <td width="50%">
          <div class="blue-box">
            <div class="part">
              <div class="part-title">
                <p>objectives</p>
              </div>
              {render_list(norm.objectives, language_1)}
            </div>
          </div>
        </td>
        <td width="*">
          <div class="blue-box">
            <div class="part">
              <div class="part-title">
                <p>objectives</p>
              </div>
              {render_list(norm.objectives, language_2)}
            </div>
          </div>
        </td>
      </tr>
      <tr>
        <td width="50%">
          <div class="blue-box">
            <div class="part">
              <div class="part-title">
                <p>risks</p>
              </div>
              {render_list(norm.risks, language_1)}
            </div>
          </div>
        </td>
        <td width="*">
          <div class="blue-box">
            <div class="part">
              <div class="part-title">
                <p>risks</p>
              </div>
              {render_list(norm.risks, language_2)}
            </div>
          </div>
        </td>
      </tr>
      <tr>
        <td width="50%">
          <div class="part">
            <div class="part-title">
              <p>drivers</p>
            </div>
            {"" if norm.drivers is None else render_drivers(norm.drivers, language_1)}
          </div>
        </td>
        <td width="*">
          <div class="part">
            <div class="part-title">
              <p>drivers</p>
            </div>
            {"" if norm.drivers is None else render_drivers(norm.drivers, language_2)}
          </div>
        </td>
      </tr>
      <tr>
        <td width="50%">
          <div class="part">
            <div class="part-title">
              <p>indicators</p>
            </div>
        </td>
        <td width="*">
          <div class="part">
            <div class="part-title">
              <p>indicators</p>
            </div>
        </td>
      </tr>
      {
        "\n".join(
            render_indicator(indicator, language_1, language_2) for indicator in norm.indicators
        )
      }
      <tr>
        <td width="50%">
          <div class="part">
            <div class="part-title">
              <p>references</p>
            </div>
        </td>
        <td width="*">
          <div class="part">
            <div class="part-title">
              <p>references</p>
            </div>
        </td>
      </tr>
      <tr>
      {
        ""
        if norm.references is None
        else "\n      </tr>\n      <tr>".join(
            f'''
            <td>{render_reference(reference, language_1)}</td>
            <td>{render_reference(reference, language_2)}</td>
            '''
            for reference in norm.references
        )
      }
      </tr>
    </table>
  </body>
</html>
    """.strip()  # fmt: skip
