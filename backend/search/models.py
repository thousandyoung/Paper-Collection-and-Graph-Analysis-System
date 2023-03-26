from neomodel import StructuredNode, StringProperty, DateTimeProperty, IntegerProperty, UniqueIdProperty, StructuredRel, RelationshipTo, RelationshipFrom, Relationship

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

class CoOccurrence(StructuredRel):
    weight = IntegerProperty(default=0) 

class Keyword(StructuredNode):
    name = StringProperty()
    
    papers = RelationshipFrom('Paper', 'HAS_KEYWORD')
    co_occurrence = Relationship('Keyword', 'CO_OCCURRENCE', model=CoOccurrence)
