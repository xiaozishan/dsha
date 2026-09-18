# -*- coding: utf-8 -*-
"""DSHA 图标深色化：从 mipmap-xxxhdpi/ic_launcher.png 生成
1) adaptive icon 前景层（432x432，中央安全区）
2) 单色剪影层（monochrome，白色轮廓）
输出到 res/drawable-nodpi/ 与 res/mipmap-anydpi-v26/ 的 XML 由本脚本一并写入。
"""
import os, sys
from PIL import Image

MAIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                    "app", "src", "main")
SRC = os.path.join(MAIN, "res", "mipmap-xxxhdpi", "ic_launcher.png")
OUT_DRAWABLE = os.path.join(MAIN, "res", "drawable-nodpi")
OUT_ANYDPI = os.path.join(MAIN, "res", "mipmap-anydpi-v26")
BRAND_BG = "#315DB4"  # values/colors.xml 的 primary

def main():
    icon = Image.open(SRC).convert("RGBA")
    print("源图标:", icon.size)

    os.makedirs(OUT_DRAWABLE, exist_ok=True)
    os.makedirs(OUT_ANYDPI, exist_ok=True)

    # ---- 前景层：432x432 画布，原图标缩到 288（66.7% 安全区）居中 ----
    fg = Image.new("RGBA", (432, 432), (0, 0, 0, 0))
    inner = 288
    scaled = icon.resize((inner, inner), Image.LANCZOS)
    fg.paste(scaled, ((432 - inner) // 2, (432 - inner) // 2), scaled)
    fg.save(os.path.join(OUT_DRAWABLE, "ic_launcher_foreground.png"))
    print("前景层 -> drawable-nodpi/ic_launcher_foreground.png", fg.size)

    # ---- 单色层：alpha>40% -> 纯白剪影，同 432 画布 ----
    alpha = icon.split()[3].point(lambda a: 255 if a > 102 else 0)
    mono_inner = Image.new("L", (inner, inner), 0)
    a_small = alpha.resize((inner, inner), Image.LANCZOS)
    mono_inner = a_small.point(lambda a: 255 if a > 127 else 0)
    mono = Image.new("RGBA", (432, 432), (0, 0, 0, 0))
    white = Image.new("RGBA", (432, 432), (255, 255, 255, 255))
    mask = Image.new("L", (432, 432), 0)
    mask.paste(mono_inner, ((432 - inner) // 2, (432 - inner) // 2))
    mono = Image.composite(white, mono, mask)
    mono.save(os.path.join(OUT_DRAWABLE, "ic_launcher_monochrome.png"))
    print("单色层 -> drawable-nodpi/ic_launcher_monochrome.png", mono.size)

    # ---- 背景层：纯色（品牌蓝） ----
    bg_xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
              '<shape xmlns:android="http://schemas.android.com/apk/res/android" '
              'android:shape="rectangle">\n'
              '    <solid android:color="' + BRAND_BG + '" />\n'
              '</shape>\n')
    with open(os.path.join(OUT_DRAWABLE, "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
        f.write(bg_xml)
    print("背景层 -> drawable-nodpi/ic_launcher_background.xml", BRAND_BG)

    # ---- adaptive icon XML ----
    adaptive = ('<?xml version="1.0" encoding="utf-8"?>\n'
                '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
                '    <background android:drawable="@drawable/ic_launcher_background" />\n'
                '    <foreground android:drawable="@drawable/ic_launcher_foreground" />\n'
                '    <monochrome android:drawable="@drawable/ic_launcher_monochrome" />\n'
                '</adaptive-icon>\n')
    with open(os.path.join(OUT_ANYDPI, "ic_launcher.xml"), "w", encoding="utf-8") as f:
        f.write(adaptive)
    with open(os.path.join(OUT_ANYDPI, "ic_launcher_round.xml"), "w", encoding="utf-8") as f:
        f.write(adaptive)
    print("adaptive XML -> mipmap-anydpi-v26/ic_launcher(.xml) + ic_launcher_round.xml")

if __name__ == "__main__":
    main()
