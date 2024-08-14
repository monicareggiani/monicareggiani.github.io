import pandas as pd
from jinja2 import Template
from html import escape

# just a simple function to be sure it
def get_pubs(csv_url):
    pubs = pd.read_csv(csv_url, na_filter=False)
    return pubs    


def bold_author_name(authors, target_name="Reggiani M."):
    """
    Bold the target author's name in the list of authors.
    """
    authors_list = authors.split("; ")
    bolded_authors = [f"<strong>{author}</strong>" if target_name in author else author for author in authors_list]
    return ", ".join(bolded_authors)


def make_pub_working(pubs):
    # HTML template
    template_str = """
    <div class="pub"> 
    <div class="grid"> 
    <div class="g-col-11"> 
    <ol> 
    {{ authors }} ({{ year }}) “{{ title }}” <em>{{ journal }}</em>.  Publication Stage: {{ stage }}
    </ol>  
    </div> 
    <div class="g-col-1"> 
    </div> 
    </div>
    <ul style="list-style: none;">
    
    </div> 
    <aside> 
    </aside>
    """
    
    # Initialize the template
    template = Template(template_str)
    
    html_output = ""
    # Generate HTML for each row with the specified category
    for _, row in pubs.iterrows():
        # Render the template with the row data
        html_output += template.render(authors=bold_author_name(row['authors']),
                                        year=row['year'],
                                        title=row['title'],
                                        journal=row['source_title'],
                                        stage=row['Publication Stage'])
    
    return html_output




def make_icon_text(icon, text):
    """
    Helper function to create the HTML for the icon and text.
    """
    return f'<i class="{escape(icon)}"></i> {escape(text)}' if text else f'<i class="{escape(icon)}"></i>'

def icon_link(icon=None, text=None, url=None, class_name="icon-link", target="_blank"):
    """
    Create an HTML link with an icon.
    """
    if icon:
        text = make_icon_text(icon, text)
    
    # Ensure all parameters are strings
    url = str(url)
    class_name = str(class_name)
    target = str(target)
    
    return f'<a href="{escape(url)}" class="{escape(class_name)}" target="{escape(target)}" rel="noopener">{text}</a>'


def make_html_icons(pub):

    html = []

    if pub.get('summary'):
        html.append(icon_link(
            icon="fas fa-external-link-alt",
            text="Summary",
            url=pub['url_summary'],
            class_name="icon-link-summary",
            target="_self"
        ))

    if pub.get('url_pub'):
        html.append(icon_link(
            icon="fas fa-external-link-alt",
            text="View",
            url=pub['url_pub']
        ))
    
    if pub.get('url_pdf'):
        html.append(icon_link(
            icon="fa fa-file-pdf",
            text="PDF",
            url=pub['url_pdf']
        ))
    
    if pub.get('url_repo'):
        html.append(icon_link(
            icon="fab fa-github",
            text="Code & Data",
            url=pub['url_repo']
        ))
    
    if pub.get('url_other'):
        html.append(icon_link(
            icon="fas fa-external-link-alt",
            text=pub['other_label'],
            url=pub['url_other']
        ))
    
    if pub.get('url_rg'):
        html.append(icon_link(
            icon="ai ai-researchgate",
            text="RG",
            url=pub['url_rg']
        ))
    
    if pub.get('url_scholar'):
        html.append(icon_link(
            icon="ai ai-google-scholar",
            text="Scholar",
            url=pub['url_scholar']
        ))

    return ''.join(html)


def make_pub_list(pubs, category):
    # HTML template
    template_str = """
    <div class="pub"> 
    <div class="grid"> 
    <div class="g-col-11"> 
    <ol> 
    {{ authors }} ({{ year }}) “{{ title }}” <em>{{ journal }}</em>.  DOI: <a href="http://doi.org/{{ doi }}">{{ doi }}</a>
    </ol>  
    </div> 
    <div class="g-col-1"> 
    <span class="__dimensions_badge_embed__" data-doi="{{ doi }}" data-hide-zero-citations="true" data-legend="hover-right" data-style="small_circle"></span><script async src="https://badge.dimensions.ai/badge.js" charset="utf-8"></script>
    </div> 
    </div>
    <ul style="list-style: none;">
    {{ icons }}
    </div> 
    <aside> 
    </aside>
    """
    
    # Initialize the template
    template = Template(template_str)
    
    html_output = ""
    # Generate HTML for each row with the specified category
    for _, row in pubs.iterrows():
        if row['Document Type'] == category:
            # Render the template with the row data
            icons_html = make_html_icons(row)
            html_output += template.render(authors=bold_author_name(row['authors']),
                                           year=row['year'],
                                           title=row['title'],
                                           journal=row['source_title'],
                                           doi_link=row['DOI'],
                                           doi=row['DOI'],
                                           icons = icons_html)
    
    return html_output



#### OLD perfect for jhelvy's csv formato
def generate_html_for_category(pubs, category):
    # HTML template
    template_str = """
    <div class="pub"> 
    <div class="grid"> 
    <div class="g-col-11"> 
    <ol> 
    {{ authors }} ({{ year }}) “{{ title }}” <em>{{ journal }}</em>.  DOI: <a href="{{ doi_link }}">{{ doi }}</a>
    </ol>  
    </div> 
    <div class="g-col-1"> 
    <div data-badge-type="donut" data-doi="{{ doi }}" data-hide-no-mentions="true" class="altmetric-embed"></div> 
    </div> 
    </div>
    <ul style="list-style: none;">
    <li>
    </div> 
    <aside> 
    </aside>
    """
    
    # Initialize the template
    template = Template(template_str)
    
    html_output = ""
    # Generate HTML for each row with the specified category
    for _, row in pubs.iterrows():
        if row['category'] == category:
            # Render the template with the row data
            html_output += template.render(authors=bold_author_name(row['author']),
                                           year=row['year'],
                                           title=row['title'],
                                           journal=row['journal'],
                                           doi_link=row['doi'],
                                           doi=row['doi'])
    
    return html_output