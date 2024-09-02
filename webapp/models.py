
# Model (tables) for the relational database (SQLite)

# Import Django model
from django.db import models 
from django.contrib.auth.models import User


# Create our tables
class Code(models.Model):
	# Each code is related to ONE User (one-to-many), code remains if user gets deleted
	user = models.ForeignKey(User, related_name='code', on_delete=models.DO_NOTHING)
	question = models.TextField(max_length=300) # Keep this low to prevent expensive API-tool
	code_answer = models.TextField(max_length=400) # Keep this low
	language = models.CharField(max_length=50) # Keep this low

	# If classobject is printed
	def __str__(self):
		return self.question



