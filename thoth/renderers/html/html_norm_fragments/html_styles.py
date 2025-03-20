# standard library imports

# third party imports

# own imports


def render() -> list[str]:
    return [
        """
    <style>
      <!-- standard elements -->
      table {
        border-collapse: separate;
        border-spacing: 0px 6px;
        margin: 24px 0px;
      }
      th, td {
        vertical-align: top;
        padding: 4px;
      }
      ul {
        list-style-type: "- ";
      }
    </style>
    <style>
      <!-- custom classes -->
      .blue-box {
        background-color: #DDE8F6;
        margin: -1px;
        padding: 1px;
      }
      .norm-title {
        margin: 12px 0px;
        padding: 4px 6px;
        font-weight: bold;
        font-size: larger;
        color: white;
        background-color: #325899;
      }
      .norm-intro {
        font-style: italic;
      }
      .part {
        margin: 0px 6px;
      }
      .part-title {
        margin: 6px 0px;
        font-weight: bold;
        font-size: larger;
      }
      .sub-part {
        margin: 16px 6px;
      }
      .sub-part-title {
        margin: 6px 0px;
        font-weight: bold;
        font-size: medium;
      }
      .sub-sub-part {
        margin: 16px 0px;
      }
      .sub-sub-part-title {
        margin: 6px 0px;
        font-weight: bold;
        font-size: medium;
        color: #2E5E7E;
      }
      .indicator-title {
        padding: 4px 6px;
        margin: 6px 0px;
        color: white;
        background-color: #325899;
      }
      .reference {
      }
    </style>
    <style>
      .footer {
        font-size: 50%;
        margin-top: 16px;
      }
    </style>
        """
    ]