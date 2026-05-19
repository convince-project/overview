import oracle

# property to verify
# During a Place, the effort shall not exceed 4.5N for more than Delta seconds (here 200ms)
PROPERTY = "( {PLACE} -> ( once[0:0.2]( {effort <= 4.5} ) ) )"

# declaration of predicates used in the property (initialization at time 0)
predicates = dict(
    time = 0,
    IDLE = True,
    PICK = False,
    NAVIGATE = False,
    PLACE = False,
    effort = 0.0,
)

# function to abstract a dictionary (obtained from Json message) into a list of predicates
# the behavior of the function must be defined by the user depending on the property and topic/service message
def abstract_message(message):
    predicates['time'] = message['time']
    predicates['effort'] = message['data'] if message['topic'] == 'robot/force_effort_z' else predicates['effort']
    predicates['IDLE'] = message['data'] == 'IDLE' if message['topic'] == 'robot/exec_action_name' else predicates['IDLE']
    predicates['PICK'] = message['data'] == 'PICK' if message['topic'] == 'robot/exec_action_name' else predicates['PICK']
    predicates['NAVIGATE'] = message['data'] == 'NAVIGATE' if message['topic'] == 'robot/exec_action_name' else predicates['NAVIGATE']
    predicates['PLACE'] = message['data'] == 'PLACE' if message['topic'] == 'robot/exec_action_name' else predicates['PLACE']
    return predicates
