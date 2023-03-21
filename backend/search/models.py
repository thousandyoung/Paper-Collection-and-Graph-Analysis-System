from neomodel import StructuredNode, StringProperty, DateTimeProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom

class Paper(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(unique_index=True)
    abstract = StringProperty()
    link = StringProperty()
    published_date = DateTimeProperty()
    crawl_time = DateTimeProperty()
    
    authors = RelationshipFrom('Author', 'WROTE')
    keywords = RelationshipTo('Keyword', 'HAS_KEYWORD')
    
class Author(StructuredNode):
    name = StringProperty()
    department_name = StringProperty()

    papers = RelationshipTo('Paper', 'WROTE')
    department = RelationshipTo('Department', 'BELONGS_TO')
    
class Department(StructuredNode):
    name = StringProperty()
    
    authors = RelationshipFrom('Author', 'BELONGS_TO')
    
class Keyword(StructuredNode):
    name = StringProperty()
    
    papers = RelationshipFrom('Paper', 'HAS_KEYWORD')
