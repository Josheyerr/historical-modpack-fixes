from pathlib import Path

WORKSHOP = Path(r"F:\bap ce compatch\workshop")
OUT = Path(r"C:\ck3_workshop_upload\historical_modpack_fixes_page.vdf")
CHANGENOTE = "Workshop page cleanup: new description layout and images. Mod files unchanged."


def esc(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def main() -> None:
    file_id = (WORKSHOP / "publishedfileid.txt").read_text().split()[0]
    description = (WORKSHOP / "description.txt").read_text(encoding="utf-8").strip()
    # No contentfolder or previewfile: SteamCMD then updates only the page text.
    fields = {
        "appid": "1158310",
        "publishedfileid": file_id,
        "title": "Josheyer Historical Modpack Fixes",
        "description": description,
        "changenote": CHANGENOTE,
    }
    body = "\n".join(f'\t"{k}"\t\t"{esc(v)}"' for k, v in fields.items())
    OUT.write_text('"workshopitem"\n{\n' + body + "\n}\n", encoding="utf-8")
    print(OUT, file_id, len(description), "chars")


if __name__ == "__main__":
    main()
