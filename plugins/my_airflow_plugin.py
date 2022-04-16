from airflow.plugins_manager import AirflowPlugin
from hooks.awx_hook import *
from operators.awx_operator import *
                    
class PluginName(AirflowPlugin):
                    
    name = 'Adts_plugin'
                    
    hooks = [AWXHook]
    operators = [AWXOperator]
    