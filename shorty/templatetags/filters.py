from django import template


register = template.Library()


@register.filter(name='classes_and_placeholder')
def classes_and_placeholder(value, args):
    arg_list = args.split(' ')
    return value.as_widget(attrs={'class': ' '.join(arg_list[:-1]), 'placeholder': arg_list[-1]})
