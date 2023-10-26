# Main agent class 
from opus.llm import initialize_llm
from opus.prompts import *
from yaspin import yaspin
from langchain.chains import LLMChain
import string
import ast
from opus.utils import *

class Agent:
    def __init__(self, ctx):
        self.ctx = ctx
        self.history = []
        self.llm = initialize_llm(self.ctx)
        self.types = ["physobj", "location", "direction", "agent", "concept"]

    def current_utterance(self):
        return self.history[-1]['value']

    def parse(self, utterance):
        self.history.append({"from": "human", "value": utterance, "parses":[]})
        self.ctx['history'] = self.history
        self.smr = {"referents": [], "intention": {}, "descriptors":[]} 
        varcount = 0

        # get speech act or intent
        intent = self._get_intent()
        self.smr['intention']['intent'] = intent
        
        # get central referent 
        central_ref = self._get_central_ref()
        self.smr['referents'].append(central_ref)
        
        # get supplemental referents
        supp_refs = self._get_supp_refs()
        self.smr['referents'].extend(supp_refs)

        # let's add some variable names
        for ref in self.smr['referents']:
            if not "variable_name" in ref:
                ref['variable_name'] = f"VAR{varcount}"
                varcount += 1

        # get CPC
        self.smr['intention']['proposition'] = self._get_cpc()

        # get SPCs
        self.smr['descriptors'] = self._get_descriptors()


        # get cognitive_statuses
        cognitive_statuses = self._get_cognitive_status()
        for ref in self.smr['referents']:
            if "variable_name" in ref:
                varname = ref['variable_name']
                status = cognitive_statuses[varname]
                ref['cognitive_status'] = status


        # Save parse
        self.history[-1]['parses'].append(self.smr)
        return self.smr
    

    @yaspin(text="Intent...", color="yellow")
    def _get_intent(self):
        chain_speech_act = LLMChain(llm=self.llm, prompt=prompt_speech_act)
        if self.ctx['verbose']:
            print("prompt: ", prompt_speech_act)
        intent = chain_speech_act.run(utterance=self.current_utterance(),
                                        history=self.history[:-1]).lower()
        return intent


    @yaspin(text="Central referent...", color="blue")
    def _get_central_ref(self):
        chain_centralref = LLMChain(llm=self.llm, prompt=prompt_centralref)
        chain_typeof = LLMChain(llm=self.llm, prompt=prompt_typeof)
        if self.ctx['verbose']:
            print("prompt: ", prompt_centralref)
        centralref = chain_centralref.run(utterance=self.current_utterance(),
                                        history=self.history[:-1]).lower()
        centralref_type = chain_typeof.run(ref=centralref, types=self.types, utterance=self.current_utterance()).split(" ")[-1]
        centralref_type = centralref_type.translate(str.maketrans('', '', string.punctuation))
        ref = {"text": centralref,
               "type": centralref_type,
               "role": "central"}
        
        return ref

    @yaspin(text="Supplementary referents...", color="magenta")
    def _get_supp_refs(self):
        
        #chains 
        chain_suppref = LLMChain(llm=self.llm, prompt=prompt_suppref)
        chain_typeof = LLMChain(llm=self.llm, prompt=prompt_typeof)

        supprefs = chain_suppref.run(utterance=self.current_utterance(), centralref=self.central_referent(self.smr)).lower()
        supprefs = ast.literal_eval(supprefs)
        
        referents = []
        #supprefs_full = [] #with type info
        if supprefs:
            for suppref in supprefs:
                suppref_type = chain_typeof.run(ref=suppref, types=self.types, utterance=self.current_utterance()).split(" ")[-1]
                
                referents.append({"text": suppref, 
                                "type": suppref_type, 
                                "role": "supplemental"})
        return referents

    @yaspin(text="Central Proposition (CPC)...", color="cyan")
    def _get_cpc(self):
        chain_cpc = LLMChain(llm=self.llm, prompt=prompt_cpc)
        
        cpc = chain_cpc.run(utterance=self.current_utterance(), 
                            speechact=self.smr['intention']['intent'], 
                            centralref=self.central_referent(self.smr))
        
        return {"text": cpc.split(":")[0], "type": cpc.split(":")[-1]}
    

    @yaspin(text="Supplementals Descriptors (SPCs)...", color="white")
    def _get_descriptors(self):
        chain_properties = LLMChain(llm=self.llm, prompt=prompt_properties)

        spc = chain_properties.run(utterance=self.current_utterance(),
                                   referent_info=self.smr['referents'],
                                   cpc=self.smr['intention']['proposition'])
        descriptors = ast.literal_eval(spc)
        return descriptors
    
    @yaspin(text="Cognitive Status", color="yellow")
    def _get_cognitive_status(self):

        chain_cognitive_status = LLMChain(llm=self.llm, prompt=prompt_cognitive_status)
        cognitive_statuses = chain_cognitive_status.run(utterance=self.current_utterance(),
                                                   referent_info=self.smr['referents'])
        
        cognitive_statuses = ast.literal_eval(cognitive_statuses)
        
        return cognitive_statuses
        
    #### UTILITY 

    def central_referent(self, smr):
        return find_dict_in_list(smr['referents'], "role", "central")

    def supp_referents(self, smr):
        return find_all_dicts_in_list(smr['referents'], "role", "supplemental")



