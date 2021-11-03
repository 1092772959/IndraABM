from enum import Enum, auto
from APIServer.model_api import run_model, create_model, create_model_for_test

# All the function that can be run on a model to get info must be defined here
class CommunicationType(Enum):
  RUN_MODEL = auto()
  AGENT_INFO = auto()

class Message:
  def __init__(self, communication_type, data):
    self.type = communication_type
    self.data = data

# This function is run in each process that is created for a model
def createModelProcess(conn, model_id, payload, indra_dir, exec_key):
    model = create_model(model_id, payload, indra_dir, exec_key)
    conn.send(model)                            # The first time a process is created, it send back the model was created
    while True:                                 # The process then goes into an infinite loop listening on the pipe
        message = conn.recv()
        if message.type == CommunicationType.RUN_MODEL:
          periods = message.data.runtime
          model.runN(int(periods))
          conn.send(model)
