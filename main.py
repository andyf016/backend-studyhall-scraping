"""
Scrape car data and recreate an HTML page.

URL: https://www.autoblog.com/classifieds/

TODO:
- get HTML of site to scrape
- read contents of the HTML
- extract specific data we want
    - year
    - make
    - price
- display extracted data
    - write to a new html file
"""
import re
import requests

template_start = "<html><body><div><ul>"
template_end = "</ul></div></body></html>"


def main():
    html = requests.get(
        'https://www.autoblog.com/sell-your-own/listings/').text
    pattern = r'src="(//s.aolcdn.com/\S+)" alt="(\d{4}) (\w+) (\w+)"'
    car_matches = re.findall(pattern, html)
    car_matches.sort(key=lambda t: t[1])  # sort cars by year
    cars = {}
    with open('cars.html', 'w') as f:
        f.write(template_start)
        if car_matches:
            for car_match in car_matches:
                img_src, year, make, model = car_match
                title = f'{year} {make} {model}'
                cars.setdefault(title, [])
                cars[title].append(img_src)
            for title, img_srcs in cars.items():
                f.write(f"<li><h3>{title}</h3>")
                for image_src in img_srcs:
                    f.write(f"""
                    <img src="https:{image_src}" alt="{title}"
                    width="200" height="140"/>
                    """)
                f.write("</li>")
        else:
            print('<li>No car found!</li>')
        f.write(template_end)


if __name__ == "__main__":
    main()
