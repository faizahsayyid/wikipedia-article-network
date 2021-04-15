# else:
#     if tag == "a" and len(self.articles) < self.sources_wanted:
#         for attribute in attrs:
#             name, link = attribute
#
#             unwanted_page = any((unwanted in link) for unwanted in UNWANTED)
#
#             if name == "href" and link.startswith('/wiki/') and not unwanted_page:
#                 self.articles.append('https://en.wikipedia.org' + link)


# if self._found_info_box and tag == 'p':
#     self._found_summary = True
# elif tag == 'table':
#     for attribute in attrs:
#         name, value = attribute
#         if name == 'class' and ('infobox' in value):
#             self._found_info_box = True


# def _count_appearances_in_article(url: str, article_name: str) -> int:
#     try:
#         data_to_parse = urllib.request.urlopen(url)
#         html = data_to_parse.read().decode()
#         data_to_parse.close()
#
#         return html.count(article_name)
#
#     except urllib.error.HTTPError:
#         return 0
