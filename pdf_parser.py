import pdfplumber
import regex as re
import nltk
import pandas as pd
def normal_func(page, Gender_guardian, Gender_voter, Guardian_name, Voter_id, Voter_name, Voter_age, index, no_label):
    # Number of rectangles
    num_rects = len(page.rects)
    for j in range(0, num_rects):
        txt_list = []
        
        # Bounding shape used for cropping the main image(pdf)
        bound = (float(page.rects[j]['x0']), float(page.rects[j]['top']), float(page.rects[j]['x1']), float(page.rects[j]['bottom']))
        c = page.crop(bbox=bound)
        
        # c represents the cropped image
        txt = c.extract_words()
        for k in range(0, len(txt)):
            
            # Storing all the strings of specific rectangle in txt_list
            txt_list.append(txt[k]['text'])
            
            # Height is same for all rectangles
            # D & T is being searched to know if that voter is labeled 'Deleted'
            # Father, Mother and Husband is searched because some rectangles have missed these labels
        if ((float(c.height) > 69.6) & (float(c.height) < 75.6)) & (('D' not in txt_list) & ('T' not in txt_list)) & (('Father\'s' in txt_list) | ('Mother\'s' in txt_list) | ('Husband\'s' in txt_list)):
            
            # Retrieving specified info from rectangles
            # txt is in dict format
            
            if ('Father\'s' in txt_list) | ('Husband\'s' in txt_list):
                Gender_guardian.append('Male')
            else:
                Gender_guardian.append('Female')
            if re.search('\d+', txt[0]['text']) == None:
                l1 = 1
            else:
                l1 = 0
            
            index.append(txt[l1]['text'])
            Voter_id.append(txt[l1+1]['text'])
            j1 = l1+4
            t = []
            while (txt[j1]['text'] not in l):
                t.append(txt[j1]['text'])
                j1+=1
            Voter_name.append(' '.join(t))
            j1+=1
            t1 = []
            while txt[j1]['text']!='House':
                t1.append(txt[j1]['text'])
                j1+=1
            t1[0] = t1[0].replace(t1[0], t1[0].split(':')[1])
            Guardian_name.append(' '.join(t1))
            if ':' in txt[-1]['text']:
                Voter_age.append(txt[-2]['text'].split(':')[1])
            else:
                Voter_age.append(txt[-1]['text'])
            if ':' in txt[-3]['text']:
                Gender_voter.append(txt[-2]['text'])
            else:
                Gender_voter.append(txt[-3]['text'])
                
        elif (('Father\'s' in txt_list) & ('Mother\'s' in txt_list) & ('Husband\'s' in txt_list)) & ('Elector\'s' in txt_list):
            no_label.append(c.extract_text())
            
    print('Completed processing pdf(Normal func)')
	def addition_func(k, Gender_guardian, Gender_voter, Guardian_name, Voter_id, Voter_name, Voter_age, index, no_label):
    flattened = [val for sublist in k.extract_tables() for val in sublist]
    flag = 0
    while (flag==0):
        flag = 1
        flattened = [val for sublist in flattened for val in sublist]
        for i in range(0, len(flattened)):
            if type(flattened[i])=='list':
                flag = 0
    flattened = [i for i in flattened if i]
    for i in range(0, len(flattened)):
        if ('Elector' in flattened[i]) & (('Father' in flattened[i]) | ('Mother' in flattened[i]) | ('Husband' in flattened[i])):
            ind1 = flattened[i].split('\n')[0].split(' ')[0]
            index.append(ind1)
            tag = flattened[i].split('\n')[0].split(' ')[2]
            Voter_id.append(tag)
            f = flattened[i][len(ind1)+len(tag)+2:]
            f_list = f.split('\n')
            s_f = f_list[-1].split(' ')
            Gender_voter.append(s_f[1])
            Voter_age.append(s_f[-1].split(':')[1])
            f_list = f_list[:-2]
            tokens = nltk.word_tokenize(','.join(f_list))[5:]
            if 'Husband' in tokens:
                id1 = tokens.index('Husband')
                Gender_guardian.append('Male')
            elif 'Father' in tokens:
                id1 = tokens.index('Father')
                Gender_guardian.append('Male')
            else:
                id1 = tokens.index('Mother')
                Gender_guardian.append('Female')
            tl = tokens[id1+4:]
            if ',' in tl:
                tl.remove(',')
            Guardian_name.append(' '.join(tl))
            tl = tokens[:id1-1]
            if ',' in tl:
                tl.remove(',')
            Voter_name.append(' '.join(tl))
        elif (('Father' not in flattened[i]) & ('Mother' not in flattened[i]) & ('Husband' not in flattened[i])) & ('Elector' in flattened[i]):
            no_label.append(flattened[i])
        print('Completed processing pdf(Addition func)')   
		
		def deletion_func(k, ind):
    if 'DELETIONS LIST' in k.extract_text():
        flattened = [val for sublist in k.extract_tables() for val in sublist]
        flag = 0
        while (flag==0):
            flag = 1
            flattened = [val for sublist in flattened for val in sublist]
            for i in range(0, len(flattened)):
                if type(flattened[i])=='list':
                    flag = 0
        flattened = [i for i in flattened if i]
    else:
        return
    for i in range(0, len(flattened)):
        if ('Elector' in flattened[i]) & (('Father' in flattened[i]) | ('Mother' in flattened[i]) | ('Husband' in flattened[i])):
            ind.append(re.search('\d+', flattened[i].split('\n')[0].split(' ')[2]).group(0))
    print('Completed processing pdf(Deleted func)')
	
	def correction_func(page, Gender_guardian, Gender_voter, Guardian_name, Voter_id, Voter_name, Voter_age, index):
    # Number of rectangles
    num_rects = len(page.rects)
    for j in range(0, num_rects):
        txt_list = []
        
        # Bounding shape used for cropping the main image(pdf)
        bound = (float(page.rects[j]['x0']), float(page.rects[j]['top']), float(page.rects[j]['x1']), float(page.rects[j]['bottom']))
        c = page.crop(bbox=bound)
        
        # c represents the cropped image
        txt = c.extract_words()
        for k in range(0, len(txt)):
            
            # Storing all the strings of specific rectangle in txt_list
            txt_list.append(txt[k]['text'])
            
            # Height is same for all rectangles
            # D & T is being searched to know if that voter is labeled 'Deleted'
            # Father, Mother and Husband is searched because some rectangles have missed these labels
        if ((float(c.height) > 69.6) & (float(c.height) < 75.6)) & (('D' not in txt_list) & ('T' not in txt_list)) & (('Father\'s' in txt_list) | ('Mother\'s' in txt_list) | ('Husband\'s' in txt_list)):
            
            # Retrieving specified info from rectangles
            # txt is in dict format
            
            if ('Father\'s' in txt_list) | ('Husband\'s' in txt_list):
                Gender_guardian.append('Male')
            else:
                Gender_guardian.append('Female')
            if re.search('\d+', txt[0]['text']) == None:
                l1 = 1
            else:
                l1 = 0
            
            del_ind = index.index(txt[l1]['text'])
            # Clearing the lists
            del index[del_ind]
            del Voter_id[del_ind]
            del Guardian_name[del_ind]
            del Gender_guardian[del_ind]
            del Gender_voter[del_ind]
            del Voter_name[del_ind]
            del Voter_age[del_ind]
            
            index.append(txt[l1]['text'])
            Voter_id.append(txt[l1+1]['text'])
            j1 = l1+4
            t = []
            while (txt[j1]['text'] not in l):
                t.append(txt[j1]['text'])
                j1+=1
            Voter_name.append(' '.join(t))
            j1+=1
            t1 = []
            while txt[j1]['text']!='House':
                t1.append(txt[j1]['text'])
                j1+=1
            t1[0] = t1[0].replace(t1[0], t1[0].split(':')[1])
            Guardian_name.append(' '.join(t1))
            if ':' in txt[-1]['text']:
                Voter_age.append(txt[-2]['text'].split(':')[1])
            else:
                Voter_age.append(txt[-1]['text'])
            if ':' in txt[-3]['text']:
                Gender_voter.append(txt[-2]['text'])
            else:
                Gender_voter.append(txt[-3]['text'])
    print('Completed processing pdf(Correction func)')
	
	def main_func(path, no_label):
    pdf = pdfplumber.open(path)

    Gender_guardian = []
    Gender_voter = []
    index = []
    Voter_id = []
    Guardian_name = []
    Voter_name = []
    Voter_age = []
    ind = []
    main_flag = 0


    for i in range(0, len(pdf.pages)):

        # Number of pages
        k = pdf.pages[i]

        if ('ADDITIONS LIST' in k.extract_text()):
            main_flag = 1
        elif 'DELETIONS LIST' in k.extract_text():
            main_flag = 2
        elif ('CORRECTION LIST' in k.extract_text()):
            main_flag = 3

        if main_flag == 0:
            normal_func(k, Gender_guardian, Gender_voter, Guardian_name, Voter_id, Voter_name, Voter_age, index, no_label)
        elif main_flag == 1:
            addition_func(k, Gender_guardian, Gender_voter, Guardian_name, Voter_id, Voter_name, Voter_age, index, no_label)
        elif main_flag == 2:
            deletion_func(k, ind)
        elif main_flag == 3:
            correction_func(k, Gender_guardian, Gender_voter, Guardian_name, Voter_id, Voter_name, Voter_age, index)
    
    print(no_label)
    
    data = pd.DataFrame()
    data['index'] = pd.Series(index)
    data['Voter_id'] = pd.Series(Voter_id)
    data['Voter_name'] = pd.Series(Voter_name)
    data['Gender_Voter'] = pd.Series(Voter_age)
    data['Voter_age'] = pd.Series(Gender_voter)
    data['Guardian_name'] = pd.Series(Guardian_name)
    data['Gender_guardian'] = pd.Series(Gender_guardian)
    
    data['index'] = data['index'].astype('int')
    
    data = data.sort_values(ascending=True, by='index')
    
    data = data[~(data.index.isin(ind))]
    
    f_name = path[len(path)-7:len(path)-3]
    
    data.to_csv(f_name+'csv', index=False)
	
	
	
