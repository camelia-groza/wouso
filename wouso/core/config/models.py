from django.db import models

class Setting(models.Model):
    """ Generic configuration (name, value) pair definition, stored in db """
    name = models.CharField(max_length=100, primary_key=True)
    value = models.TextField(default='', null=True, blank=True)

    def set_value(self, v):
        """ value setter, overriden by subclasses """
        self.value = v
        self.save()

    def get_value(self):
        """ value getter, overriden by subclasses """
        return self.value

    def form(self):
        """ Get HTML form input and label. """
        return '<label for="%s">%s</label><textarea name="%s" id="%s">%s</textarea>' \
                    % (self.name, self.title, self.name, self.name, self.value)

    @classmethod
    def get(kls, name):
        """ Get or create a Setting with the name name """
        obj, new = kls.objects.get_or_create(name=name)
        return obj

    @property
    def title(self):
        """ Capitalize name to create a setting title for display """
        if self.name.startswith('disable-'):
            return self.name[8:].capitalize()
        return self.name.capitalize().replace('_', ' ')

    def __unicode__(self):
        return self.name

class HTMLSetting(Setting):
    """ Setting storing a generic text or HTML """
    class Meta:
        proxy = True

class BoolSetting(Setting):
    """ Setting storing boolean values (as string True/False) """
    class Meta:
        proxy = True

    def set_value(self, b):
        if isinstance(b, bool):
            self.value = 'True' if b else 'False'
        else:
            self.value = b
        self.save()

    def get_value(self):
        return (self.value == 'True')

    def form(self):
        return '<label for="%s">%s</label><input type="checkbox" name="%s" id="%s" %s value="True" />' \
                    % (self.name, self.title, self.name, self.name, 'checked' if self.get_value() else '')

class ChoicesSetting(Setting):
    """ Setting storing string values, but having a choices list of tuple
    (value, text) choices
    """
    class Meta:
        proxy = True

    choices = []

    def form(self):
        html = '<label for="%s">%s</label><select id="%s" name="%s">' % (self.name, self.title, self.name, self.name)
        for n,v in self.choices:
            html += '<option value="%s" %s>%s</option>' % (v, 'selected' if self.value == v else '', n)
        html += '</select>'
        return html
