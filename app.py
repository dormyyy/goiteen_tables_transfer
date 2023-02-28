import os
from dotenv import load_dotenv
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()