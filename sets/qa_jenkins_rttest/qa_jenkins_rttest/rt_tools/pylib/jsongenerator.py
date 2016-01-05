import json
import warnings
import os
import pickle
import random

class JsonGenerator(object):
    
    def __init__(self, file_name):

        self.step_data = []
        self.scen_data = []
        self.feat_data = []
        self.file_name = file_name
        
    def addStep(self, step_name, step_status='passed', step_duration=0, step_keyword="TestCase:",
                     step_err_msg="", step_desc=None, step_output=None, step_doc=None, step_url=None):

        if step_desc:
            if type(step_desc) == type({}):
                if 'description' in step_desc:
                    step_desc_data = step_desc
                else:
                    step_desc_data = {}
                    warnings.warn("Error : Please pass correct data. eg:{\'description':\"Description for step\"}")
            elif type(step_desc) == type(''):
                step_desc_data = {'description':"%s" %step_desc}
            else:
                step_desc_data = {}
                warnings.warn("Error : Please pass correct data. eg:{\'description':\"Description for step\"},"
                              " \"This is description info\"")
        else:
            step_desc_data = {}

        # Add qadb url to step name
        if step_url:
            step_name = (step_name + " -  <a href=%s>QADB URL</a>" %step_url)
            
        if step_output:
            if type(step_output) == type({}):
                step_output_data = step_output
            elif type(step_output) == type([]):
                step_output_data = {'output':step_output}
            elif type(step_output) == type(''):
                step_output_data = {'output':[step_output]}
            else:
                step_output_data = {}
                warnings.warn("Error : Please pass correct data. eg:[\"This is step output info\"],"
                              " \"This is step output info\"")
        else:
            step_output_data = {}

        if step_doc:
            if type(step_doc) == type({}):
                if 'doc_string' in step_doc:
                    step_doc_data = step_doc
                else:
                    step_doc_data = {}
                    warnings.warn("Error : Please pass correct data. eg:{\'value':\"Doc string info for step\"}")
            elif type(step_doc) == type(''):
                step_doc_data = {'doc_string':{'value':"%s" %step_doc}}
            else:
                step_doc_data = {}
                warnings.warn("Error : Please pass correct data. eg:{\'value':\"Doc string info for step\"},"
                              " \"This is doc string info\"")
        else:
            step_doc_data = {}


        b_step_map = {'keyword':step_keyword,
                       'name':step_name,
                       'result':{'status':step_status,
                                 'error_message':(step_err_msg or "Test Case %s is failed, refer to qadb "
                                                  "for more details." %step_name),
                                 'duration':step_duration * pow(10,9)}}
        b_step_map.update(step_desc_data)
        b_step_map.update(step_output_data)
        b_step_map.update(step_doc_data)

        self.step_data.append(b_step_map)

    def addScenario(self, scen_name, scen_step=[], scen_keyword="TestSuite", scen_tags=None, scen_url=None):
        
        if scen_tags:
            if type(scen_tags) == type({}):
                scen_tags_data = scen_tags
            elif type(scen_tags) == type(''):
                scen_tags_data = {'tags':[{'name':scen_tags}]}
            else:
                scen_tags_data = {}
                warnings.warn("Error : Please pass correct data. eg:[{\'name':\"tags name\"}] or "
                              " \"This is tags name\"")
        else:
            scen_tags_data = {}

        scen_name = (scen_name + (scen_url and " |  <a href=%s>QADB URL</a>" %(scen_url) or ''))
        b_sen_map = {'keyword':scen_keyword,
                      'name':scen_name,
                      'steps':scen_step}
        self.step_data = []
        b_sen_map.update(scen_tags_data)
        
        self.scen_data.append(b_sen_map)

    def addFeature(self, feat_name, feat_desc, feat_keyword="Features", feat_elements=[], feat_tags=None):

        if feat_tags:
            if type(feat_tags) == type({}):
                feat_tags_data = feat_tags
            elif type(feat_tags) == type(''):
                feat_tags_data = {'tags':[{'name':feat_tags}]}
            else:
                feat_tags_data = {}
                warnings.warn("Error : Please pass correct data. eg:[{\'name':\"tags name\"}] or "
                              " \"This is tags name\"")
        else:
            feat_tags_data = {}
       
        b_fea_map = {'description':feat_desc,
                      'keyword':feat_keyword,
                      'name':feat_name,
                      'elements':feat_elements,
                      'uri':"%s-%d" %(feat_name, random.randint(10000,999999))}
        
        b_fea_map.update(feat_tags_data)
        
        self.feat_data.append(b_fea_map)
    
    def setEmpty2StepData(self):
        self.step_data = []

    def setEmpty2ScenData(self):
        self.scen_data = []

    def setEmpty2FeatData(self):
        self.feat_data = []
        
    def generateJsonFile(self, file, data=[]):
        feat_data = data or self.feat_data
        json_data = json.dumps(feat_data, sort_keys = True, indent = 4, )
        with open(file, "w+") as f:
            f.truncate()
            f.write(json_data)
    '''
    def dumpData(self, file_name, data):
        with open(file_name, "w+") as f:
            f.truncate()
            pickle.dump(data, f)
            
    def loadData(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                return pickle.load(f)
        else:
            return []
    '''
if __name__ == '__main__':
    ins_jsong = JsonGenerator("./f.json")
    step = ins_jsong.addStep(step_keyword="s111",
                           step_name="name",
                           step_status="passed",
                           step_duration=100)
    scen = ins_jsong.addScenario(scen_keyword="scenario", scen_name="sce1", scen_step=[])
    feat = ins_jsong.addFeature(feat_name="fffff", feat_desc="desc.......", feat_elements=ins_jsong.scen_data)
    
    ins_jsong.generateJsonFile()