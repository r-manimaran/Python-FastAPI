import logging
import logging.config
from typing import Dict

def setup_logging(default_level= logging.INFO) -> None:
   logging_config:Dict = {
      'version':1,
      'disable_existing_loggers':False,
      'formatters':{
         'standard':{
            'format':'%(asctime)s [%(levelname)s] %(name)s: %(message)s'
         },
         'detailed':{
            'format':'%(asctime)s - %(name)s - %(levelname)s -%(pathname)s:%(lineno)d- %(message)s'
         },
      },
      'handlers':{
         'console':{
            'level':'DEBUG',
            'formatter':'standard',
            'class':'logging.StreamHandler'           
         },
         'error_file':{
            'level':'ERROR',
            'formatter':'detailed',
            'class':'logging.FileHandler',
            'filename':'error.log',
            'mode':'a'
         },
         'file':{
            'level':'INFO',
            'class':'logging.FileHandler',
            'filename':'app.log',
            'formatter':'detailed',
            'mode':'a'
         }
      },
      'loggers':{
         '':{
            'handlers':['console','file','error_file'],
            'level':default_level,
            'propagate':True
         },
         'uvicorn.error':{
            'handlers':['console','file','error_file'],
            'level':'ERROR',
            'propagate':True
         },
         'uvicorn.access':{
            'handlers':['console','file'],
            'level':'INFO',
            'propagate':False
         }
      }
   }
   logging.config.dictConfig(logging_config)