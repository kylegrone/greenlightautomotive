from django.forms import ModelChoiceField

class QuestionChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.question_text
    
    
class StateChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.name
    
class TrimChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.name