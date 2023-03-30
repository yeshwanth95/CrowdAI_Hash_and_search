import json
import os


def main(json_fn):
    with open(json_fn, 'r') as f_in:
        json_data = json.load(f_in)

    # Header
    html_header = "<!DOCTYPE html>\n" \
                  "<html>\n" \
                  "<head>\n" \
                  "<style>\n" \
                  "* {\n" \
                  "  box-sizing: border-box;\n" \
                  "}\n" \
                  ".columntable {\n" \
                  "  float: left;\n" \
                  "  width: 16.66%;\n" \
                  "  padding: 5px;\n" \
                  "}\n" \
                  "/* Clearfix (clear floats) */\n" \
                  ".row::after {\n" \
                  '  content: "";\n' \
                  "  clear: both;\n" \
                  "  display: table;\n" \
                  "}\n" \
                  "</style>\n" \
                  "</head>\n"

    # Create body
    html_body = "<body>\n"
    html_body += "<h2>Duplicate images</h2>\n"
    html_body += "</body>\n"

    max_img = 70
    base_dir = os.path.join("data", "train", "images")
    for img_idx, uniq_img in enumerate(json_data.keys()):
        dup_img_list = json_data[uniq_img]
        # Add header
        html_body+= f'<h3>{img_idx}. {uniq_img.split(".")[0]}</h3>\n'
        # Create row
        html_body += '<div class="row">\n'
        # Add unique image
        html_body += f'<h4>Unique</h4>\n'
        html_body += '<div class ="columntable">\n'
        html_body += '<figure>\n'
        html_body += f'<img src = "{os.path.join(base_dir, uniq_img)}"	alt = "Image not found"	style = "width:100%">\n'
        html_body += f'<figcaption>{uniq_img.split(".")[0]}</figcaption>\n'
        html_body += '</figure>\n'
        html_body += '</div>\n'
        # Close row
        html_body += '</div>\n'

        # Add dup_img images
        # Create row
        html_body += '<div class="row">\n'
        html_body += f'<h4>Duplicates</h4>\n'
        for dup_img in dup_img_list:
            html_body += '<div class ="columntable">\n'
            html_body += '<figure>\n'
            html_body += f'<img src = "{os.path.join(base_dir, dup_img)}"	alt = "Image not found"	style = "width:100%">\n'
            html_body += f'<figcaption>{dup_img.split(".")[0]}</figcaption>\n'
            html_body += '</figure>\n'
            html_body += '</div>\n'

        # Close row
        html_body += '</div>\n'

        if img_idx+1 == max_img:
            break

    # Close html
    html_close = "</html>"

    # Create html buf
    html_buf = html_header + html_body +  html_close

    # Output html
    html_fn = "uniq_to_dup_imgs.html"
    with open(html_fn, 'w') as f_out:
        f_out.write(html_buf)


if __name__ == '__main__':
    main(json_fn="uniq_to_dup_imgs.json")
