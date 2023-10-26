# LLM Chains 
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI,ChatAnthropic

# (1) Speech Act Classification 

template_speech_act= """
Decide whether the utterance from a speaker to a listener (in the context of a chat history) is one of "INSTRUCT", "STATEMENT", "QUESTION"
An "INSTRUCT" is an imperative statement or a request by the speaker to have the listener do an action or stop doing an action.
A "QUESTION" is a 'wh' or 'yes/no' query (what, why, when, where, who) or request from a speaker for more information from the listener about the listeners knowledge, beliefs or perceptions
A "STATEMENT" is a statement of fact or opinion that the speaker conveys to a listener and  expects to listener to come to believe. 

Return only one word -- either INSTRUCT, QUESTION or STATEMENT.

context:\n{history}\n
utterance: \n{utterance}\n
intent:
"""

prompt_speech_act = PromptTemplate(
    input_variables=["utterance", "history"],
    template=template_speech_act
)



## (2) Central Referents 

template_centralref = """
What is the central item (which could be a single thing or a collection of things) that is being referred to in the below sentence (in the context of the chat history)?

Remember, the central referent is a thing or object, not an action or descriptor.It is meant to capture the central real world item being referenced in the utterance. 

Return a single word or a short span of text from the sentence.

context:\n{history}\n
sentence: \n{utterance}\n 
referent:
"""

prompt_centralref = PromptTemplate(
    input_variables=["utterance","history"],
    template=template_centralref
)

## (3) Getting the type of thing that the referents are 

template_typeof = """
Determine whether or not the referent item mentioned below in the context of the provided utterance is one of the types also provided below. To check if the referent is of a type, follow the below procedure
1. Iterate through each item mentioned in the list of types. 
2. For each item X in the list of types expand on the meaning of each item, and then ask if the central referent is of type X given that meaning. 
3. If the central referent is of type X in the list, return X.

\n\n EXAMPLE \n
utterance: The lemon is on the table
referent: lemon
types: ['area', 'physobj', 'location', 'pose']
typeOf: Looking through the items in the list of types above. physobj is a physical object. lemon is a type of physical object. So, it is of type physobj

Remember, return specifically ONE of the items in the list of types, or if none apply then return NONE. 

utterance: \n{utterance}\n
referent: \n{ref}\n
types: \n{types}\n
typeOf:
"""

prompt_typeof = PromptTemplate(
    input_variables=["ref", "types", "utterance"],
    template=template_typeof
)

## (4) Supporting Referents

template_suppref = """
What are some objects (which could be a single thing or a collection of things) that is being referred to in the below sentence not including the central referent? Return as a python list.
If none, then return empty list []. Even if only one item, return as a list.  
Remember, the supporting referents are things or objects, not actions or descriptors. They are meant to capture the real world items being referenced in the utterance. 

Do NOT include objects or collections that have already been covered in the central referent. 

Remember, return as a python list of strings.

sentence: \n{utterance}\n 
central referent: \n{centralref}\n
supporting referents (noun(s) from utterance):
"""

prompt_suppref = PromptTemplate(
    input_variables=["utterance", "centralref"],
    template=template_suppref
)


## (5) Extract CPC

template_cpc = """
Determine the core propositional content (cpc) of the utterance below in the context of its central referent and speech act type
To do so, use the following procedure

1. Determine the type of cpc ("action", "concept") associated with the utterance.
If the speech act is a "want" that means the utterance is an imperative and the cpc is an "action".
If the speech act is a "wantBel" (note the capital B) that means the utterance is a statement assertion, and the cpc will be a "concept"
If the speech act is an "itk" that means the utterance contains a question about some concept, so the cpc is a "concept"

2. If the type of cpc is an "action", then the core propositional content (or cpc) is the action that is being performed on the central referent.
If the type of cpc is a "concept", then the core propositional content (or cpc) is a concept that is being associated with the central referent.

3. Convert the cpc into a single representative word that captures its meaning, without any reference to the referents.

4. return the converted cpc and its type in the following format "<CPC>:<TYPE>" 

utterance: \n{utterance}\n
speech act: \n{speechact}\n
central referent: \n{centralref}
core propositional content and type:
"""

prompt_cpc = PromptTemplate(
    input_variables=["centralref", "utterance","speechact"],
    template=template_cpc
)

# (6) SPC Property Candidate identification 
## getting the properties of interest
## For each of the referents, we want to find any individual descriptors, we also want to find and apply any given relations between referents

template_properties = """
Determine the properties of the referents. Use the following procedure for each of the referents:
1. The names of each of the referents itself should be added as a property to the list.
2. From the utterance, extract all the adjectival descriptors used to describe the properties of the referents, and add to list.
3. Add to this list, any relations (mentioned in the utterance) between two or more of the referents. Do NOT include any relations that can be reasonably assumed to be already covered by the meaning of the core propositional content. 
4. Return this list as a list of python dictionaries with the following format:
"text": <NAME OF PROPERTY/DESCRIPTOR/RELATION -- must be a single word>, "arguments": <LIST OF VARIABLE NAMES that makes sense> 

where the variable names correspond to the variable names associated with each of the referents. Remember, the variable names have to be correct.

Remember, DO NOT include in the list anything that is semantically similar to the core propositional content since it would be redundant

utterance: \n{utterance}\n
referents: \n{referent_info}\n
core propositional content: \n{cpc}\n
supplemental properties, descriptors and relations not in the core propositional content:
"""


prompt_properties = PromptTemplate(
    input_variables=["referent_info", "utterance", "cpc"],
    template=template_properties
)

# (11) Cognitive Status

template_cognitive_status= """
Determine the cognitive status of each of the referents mentioned in the bindings. Use the following procedure for each of the referents:

1. Decide which ONE (and only one) of the following five cognitive statuses the referents could fall into:
statuses: [INFOCUS, ACTIVATED", FAMILIAR, DEFINITE, INDEFINITE]

As shown in the table below, the Givenness Hierarchy is comprised of six hierarchically nested tiers of cognitive status, 
where information with one cognitive status can be inferred to also have all
lower statuses. Each level of the GH is “cued” by a set
of linguistic forms, as seen in the table. For example, the second
row of the table shows that the definite use of “this” can be
used to infer that the speaker assumes the referent to be at
least activated to their interlocutor.
\n\n
Cognitive Status | Mnemonic Status | Form |
-----------------|-----------------|------|
INFOCUS | in the focus of attention | it |
ACTIVATED | in short term memory | this,that,this N |
FAMILIAR | in long term memory| that N |
DEFINITE | in long term memory  or new | the N |
INDEFINITE | new or hypothetical | a N |
\n\n

When deciding the one cognitive status for each referent, use the table above and compare the form (pronoun, determiner, article) of the utterance to its status.

Return this as a python dictionary using the following format for the dictionary entry. Note it MUST be a python dictionary
<VARIABLE NAME> : <COGNITIVE STATUS>

where the variable names correspond to the variable names associated with each of the referents. Remember, the variable names have to be correct.


utterance: \n{utterance}\n
referents: \n{referent_info}\n
cognitive statuses:
"""

prompt_cognitive_status = PromptTemplate(
    input_variables=["referent_info", "utterance"],
    template=template_cognitive_status
)



