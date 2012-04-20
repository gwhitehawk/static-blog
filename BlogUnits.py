import time
import re

class Article:
    def __init__(self, num_id, title, date, categories, content):
        self.num_id = num_id
        self.title = title
        self.date  = date
        self.categories = categories
        self.content = self.parse_content(content)
    
    def parse_content(self, content):
        text_gallery = content.split("Gallery:\n")
        text = re.sub( "\n", "\n<br>", text_gallery[0])
        result = text 
        
        if (len(text_gallery) == 2):
            result += "\n<br>\n"
            gallery_rows = text_gallery[1].split("\n")
            table = "<div id=\"image_wrap_%s\">\n\t<img src=\"img/blank.gif\" height=\"350\" />\n</div>\n\n" % str(self.num_id)
            table += "<a class=\"prev browse left\"></a>\n\n"
            table += "<div class=\"scrollable\">\n\t<div class=\"items\">\n"
           
            default = 1;
            for row in gallery_rows:
                new_row = "\t\t<div>\n"
                pics = row.split()
                for pic in pics:
                    new_row += "\t\t\t<img src=\"%s.jpg\" id=\"%s_%d\" />\n" % (pic, str(self.num_id), default)
                    if default:
                        default = 0
                table += new_row
                table += "\t\t</div>\n"
            
            table += "\t</div>\n</div>\n\n"
            table += "<a class=\"next browse right\"></a>"
            table += "\n<br clear=\"all\" />"
	    result += table
	return result

class Template:
    def __init__(self, file_name, css_file, title, about, categories, selected_cat, current_page, per_page, articles):
        self.file_name = file_name
        self.css_file  = css_file
        self.title     = title
        self.head      = self.create_head(title, css_file, articles)
        self.header    = self.create_header()
        self.nav       = self.create_nav(about, categories)
        self.content   = self.create_content(articles, selected_cat, current_page, per_page)
        self.html      = self.gen_html(self.head, self.header, self.nav, self.content)

    def create_head(self, title, css_file, articles):
        titles = []
        for art in articles:
            titles.append("#image_wrap_%s" % str(art.num_id))
        css_ids = ", ".join(titles)

        return """<head>
<meta name=\"MSSmartTagsPreventParsing\" content=\"TRUE\"/>
<meta http-equiv=\"expires\" content=\"-1\"/>
<meta http-equiv= \"pragma\" content=\"no-cache\"/>
<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\"/>
<meta name=\"description\" content=\"about\"/>
<link rel=\"stylesheet\" type=\"text/css\" href=\"css/%s\"/>
<link rel=\"stylesheet\" type=\"text/css\" href=\"css/scrollable-horizontal.css\"/>
<link rel=\"stylesheet \"type=\"text/css \"href=\"css/scrollable-buttons.css\"/>
<script type=\"text/javascript\" src=\"js/jquery.tools.min.js\"></script>
<script type=\"text/javascript\" src=\"js/gallery.js\"></script>
<title>%s</title>
<style>
%s
{
width:650px;
margin:15px 0 15px 40px;
padding:15px 0;
text-align:center;
background-color:#efefef;
border:2px solid #fff;
outline:1px solid #ddd;
-moz-outline-radius:4px;
}
</style>
</head>""" % (css_file, title, css_ids) 
    
    def create_header(self):
        return "\t<div id = \"header\">\n\t</div>"
         
    def create_nav(self, about, categories):
        result = "\t<div id=\"sidebar\">\n\t\t<h1>About</h1>\n\t\t%s\n\t\t<h1>Categories</h1>\n\t\t<ul id=\"sidebarnav\">\n" % about
        result += "\t\t\t<li><a href = \"index.html\">all articles</a></li>\n" 
        for cat in categories:
            result += "\t\t\t<li><a href = \"%s_1.html\">%s</a></li>\n" % (cat, cat)
        result += "\t\t</ul>\n\t</div>"
        return result

    def create_content(self, articles, selected_cat, current_page, per_page):
        article_number = len(articles)
        page_count = article_number/per_page 
        if page_count * per_page < article_number:
            page_count += 1;

        current_page_start = per_page * (current_page - 1)
        current_page_end = per_page * current_page 
        if current_page_end > article_number:
            current_page_end = article_number
        
        displayed_articles = articles[current_page_start:current_page_end]

        result = ""
        for article in displayed_articles:
            result += "\t<div class = \"content\">\n\t<h1>%s</h1>\n\t\n\t%s\n\t<br><br>\n\t%s\n\t<br>\n\tfiled in <i>%s</i>\n\t<br><br>\n\n\t</div>" % (article.title, time.strftime("%d %b %Y",article.date), article.content, ", ".join(article.categories))
 
        result += "\n\t<div id = \"footer\">\n\t<center>\n\t"
        page_links = []
        for i in range(page_count):
            if selected_cat == "":
                ref_title = self.title + "_" + str(i+1)
            else:
                ref_title = selected_cat + "_" + str(i+1)
            page_links.append( "<a href = \"%s.html\">%s</a>" % (ref_title, str(i+1)))
        
        result += ", ".join(page_links)
        result += "\n\t</center>\n\t</div>"
        return result

    def gen_html(self, head, header, nav, content):
        body_style = "<body style=\"background-image: url(back.jpg); background-repeat: ; background-color: #ffffff; \">\n<div id=\"container\">"

        result = "<!DOCTYPE html>\n<html>\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n</div>\n</body>\n</html>" % (head, body_style, header, nav, content)
        
        return result

class GenBlogPages:
    def __init__(self, title, about, css_file):
        self.title = title
        self.about = about
        self.css_file = css_file

    def create_pages(self, articles, categories, articles_per_page):
        pages = []
        categories_extended = categories + [""]

        for category in categories_extended:
            chosen_articles = []
            if category == "":
                chosen_articles = articles
            else:
                for article in articles:
                    if category in article.categories:
                        chosen_articles.append(article)
            
            article_count = len(chosen_articles)
            page_count = article_count/articles_per_page + 1

            for page_id in range(1, page_count + 1):
                if category == "":
                    file_name = self.title + "_" + str(page_id) + ".html"
                else:
                    file_name = category + "_" + str(page_id) + ".html"
                page = Template(file_name, self.css_file, self.title, self.about, categories, category, page_id, articles_per_page, chosen_articles)
                pages.append(page)

        return pages
