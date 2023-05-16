#writing validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_even(value):
	if value%2 !=0:
		raise ValidationError(
			_("%(value)s is not an even number"),
			params={'value':value}
			)

#You can add this to a model field via the field’s validators argument
from django.db import models

class MyModel(models.Model):
	even_field=models.IntegerField(validators=[validate_even])



Because values are converted to Python before validators are run, you can even use the same validator with forms:
from django import forms

class MyForm(forms.Form):
	even_field=forms.IntegerField(validators=[validate_even])


# You can also use a class with a __call__() method for more complex or configurable validators. RegexValidator, for example, uses this technique



#Built-in validators

	1-RegexValidator(regex=None, message=None, code=None, inverse_match=None, flags=0)
	2-EmailValidator(message=None, code=None, allowlist=None)
	3-URLValidator(schemes=None, regex=None, message=None, code=None)
		schemes:
			URL/URI scheme list to validate against. If not provided, the default list is ['http', 'https', 'ftp', 'ftps'].
	4-validate_email
		An EmailValidator instance without any customizations

	5-validate_slug
		A RegexValidator instance that ensures a value consists of only letters, numbers, underscores or hyphens.

	6-validate_unicode_slug
		A RegexValidator instance that ensures a value consists of only Unicode letters, numbers, underscores, or hyphens.
	7-validate_ipv4_address
	8-validate_ipv6_address
	9-validate_ipv46_address
	10-validate_comma_separated_integer_list
		A RegexValidator instance that ensures a value is a comma-separated list of integers.
	11-int_list_validator(sep=',', message=None, code='invalid', allow_negative=False)
		Returns a RegexValidator instance that ensures a string consists of integers separated by sep. It allows negative integers when allow_negative is True.

	12-MaxValueValidator(limit_value, message=None)
	13-MinValueValidator(limit_value, message=None)
	14-MaxLengthValidator(limit_value, message=None)
	15-MinLengthValidator(limit_value, message=None)
	16-DecimalValidator(max_digits, decimal_places)
	17-FileExtensionValidator(allowed_extensions, message, code)
		Raises a ValidationError with a code of 'invalid_extension' if the extension of value.name (value is a File) isn’t found in allowed_extensions. The extension is compared case-insensitively with allowed_extensions

		Don’t rely on validation of the file extension to determine a file’s type. Files can be renamed to have any extension no matter what data they contain.

	18-alidate_image_file_extension
		Uses Pillow to ensure that value.name (value is a File) has a valid image extension.
	19-rohibitNullCharactersValidator(message=None, code=None)
		Raises a ValidationError if str(value) contains one or more null characters ('\x00').

	20-StepValueValidator(limit_value, message=None)¶
		Raises a ValidationError with a code of 'step_size' if value is not an integral multiple of limit_value, which can be a float, integer or decimal value or a callable






example of StepValueValidator


Here is an example of how to use the StepValueValidator:

Python
from django.core.validators import StepValueValidator

class MyModel(models.Model):
    step_value = models.IntegerField(validators=[StepValueValidator(limit_value=10)])
Use code with caution. Learn more
This will ensure that the value of the step_value field is an integral multiple of 10. For example, the following values would be valid:

Code snippet
10
20
30
40
50
...
Use code with caution. Learn more
The following values would be invalid:

Code snippet
5
15
25
35
45
...
Use code with caution. Learn more
You can also use a callable as the limit_value argument. For example, the following code would ensure that the value of the step_value field is a multiple of the current time in seconds:

Python
from datetime import datetime

def current_time_in_seconds():
    return datetime.now().timestamp()

class MyModel(models.Model):
    step_value = models.IntegerField(validators=[StepValueValidator(limit_value=current_time_in_seconds)])
Use code with caution. Learn more
This would ensure that the value of the step_value field is always a multiple of the current time in seconds.