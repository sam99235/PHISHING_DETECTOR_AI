import re
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.naive_bayes import ComplementNB,MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report
import joblib,os
from termcolor import colored
from main import DEBUG
from datasets import load_dataset

# Load two CSV files as separate splits from the same dataset repo
dataset = load_dataset(
    "holyno/phishy_email_detector",
    data_files={
        "a": "email_dataset1.csv",
        "b": "email_dataset2.csv"
    }
)

# Convert splits to pandas DataFrames
df_a = dataset["a"].to_pandas()
df_b = dataset["b"].to_pandas()



# Combining text and labels
combined_series = pd.concat([df_a['text_combined'], df_b['body']], ignore_index=True)
combined_labels = pd.concat([df1_a['label'], df_b['label']], ignore_index=True)

# Create a DataFrame to handle both together
combined_df = pd.DataFrame({'text': combined_series, 'label': combined_labels})

# Drop rows where either text or label is NaN
combined_df = combined_df.dropna()

# Split back into X and y
X = combined_df['text']
y = combined_df['label']



# labels
# 1    42891 spam
# 0    39595 not spam

####for subjects only
#emails of emails: 82486  
A = df_b["subject"]
b = df_b["label"]
# labels
# 1    42891 spam
# 0    39595 not spam

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20,random_state=22)

A_train,A_test,b_train,b_test = train_test_split(A,b,test_size=0.20,random_state=22)



##turning textual data into a nemurical representation and doing some preprocessing

pipe_MNB = Pipeline([
    ("tfidf",TfidfVectorizer(stop_words='english',lowercase=True,max_features=15000, ngram_range=(1, 2))),
    ("clf",MultinomialNB())
])
pipe_CNB = Pipeline([
    ("tfidf",TfidfVectorizer(stop_words='english',lowercase=True,max_features=15000, ngram_range=(1, 2))),
    ("clf",ComplementNB())
])
svc = LinearSVC(
    penalty='l2',
    loss='squared_hinge',
    dual=False,
    C=4.008609717152555,
    class_weight='balanced',
    max_iter=5000
)
pipe_SVC = Pipeline([
    ("tfidf",TfidfVectorizer(stop_words='english',lowercase=True,max_features=15000, ngram_range=(1, 2))),
    ("clf",svc)
])


pipe_LR = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),  # Convert text to TF-IDF features
    ('clf', LogisticRegression())  # Apply Logistic Regression
])


body_models = {
    'model1_mnb': pipe_MNB,
    'model2_cnb': pipe_CNB,
    'model3_svc': pipe_SVC,
    'model4_lr': pipe_LR
}

save_folder = r'D:\\Desktop\\internship\\code\\saved_models'
os.makedirs(save_folder, exist_ok=True)


#email body classifer
def train_save_body_models():
    
    for name, model in body_models.items():
        file_path = os.path.join(save_folder, f'{name}.joblib')
        if not os.path.exists(file_path):
            if name =="model1_mnb":
                        if DEBUG:
                            print("NOTE=======>Training the model")
                            pipe_MNB.fit(X_train,y_train)
                            print("NOTE=======>Training is finished")
                        #model score and predictions result                        
                        train_accuracy = model.score(X_train, y_train)
                        test_accuracy = model.score(X_test, y_test)
                        if DEBUG:
                            print(f"{name} Train Accuracy:", train_accuracy)
                            print(f"{name} Test Accuracy:", test_accuracy)
                        predict_MNB = pipe_MNB.predict(X_test)
                        if DEBUG:
                            print(f"MNB => prediction::{predict_MNB}")
                            print("-"*30)
                            print(f"MNB => accuracy score::{accuracy_score(y_test,predict_MNB)}")
                            print("++++MNB",classification_report(y_test,predict_MNB))
                        #saving the model
                        joblib.dump(model, file_path)
                        if DEBUG:
                            print("-"*30)
                            print(f"Saved: {file_path}")
                            print("#"*20)

            elif name =="model2_cnb":
                        if DEBUG:
                            print("NOTE=======>Training the model")
                        pipe_CNB.fit(X_train,y_train)
                        if DEBUG:
                            print("NOTE=======>Training is finished")
                        ##model score and predictions result
                        train_accuracy = model.score(X_train, y_train)
                        test_accuracy = model.score(X_test, y_test)
                        if DEBUG:
                            print(f"{name} Train Accuracy:", train_accuracy)
                            print(f"{name} Test Accuracy:", test_accuracy)
                        predict_CNB = pipe_CNB.predict(X_test)
                        if DEBUG:
                            print(f"CNB => prediction::{predict_CNB}")
                            print("-"*30)
                            print(f"CNB => accuracy score::{accuracy_score(y_test,predict_CNB)}")
                            print("++++",classification_report(y_test,predict_CNB))
                        #saving the model
                        joblib.dump(model, file_path)
                        if DEBUG:
                            print("-"*30)
                            print(f"Saved: {file_path}")
                            print("#"*20)


            elif name =="model3_svc":
                        if DEBUG:
                              print("NOTE=======>Training the model")
                        pipe_SVC.fit(X_train,y_train)
                        if DEBUG:      
                              print("NOTE=======>Training is finished")
                        #model score and predictions result
                        train_accuracy = model.score(X_train, y_train)
                        test_accuracy = model.score(X_test, y_test)
                        if DEBUG:
                            print(f"{name} Train Accuracy:", train_accuracy)
                            print(f"{name} Test Accuracy:", test_accuracy)
                        predict_SVC = pipe_SVC.predict(X_test)
                        if DEBUG:
                            print(f"SVC => prediction::{predict_SVC}")
                            print("-"*30)
                            print(f"SVC => accuracy score::{accuracy_score(y_test,predict_SVC)}")
                            print("++++SVC",classification_report(y_test,predict_SVC))
                        #saving the model
                        joblib.dump(model, file_path)
                        if DEBUG:
                            print("-"*30)
                            print(f"Saved: {file_path}")
                            print("#"*20)
            elif name =="model4_lr":
                if DEBUG: print("NOTE=======>Training the model")
                pipe_LR.fit(X_train,y_train)
                if DEBUG: print("NOTE=======>Training is finished")
                train_accuracy = model.score(X_train, y_train)
                test_accuracy = model.score(X_test, y_test)
                if DEBUG: print(f"{name} Train Accuracy:", train_accuracy)
                if DEBUG: print(f"{name} Test Accuracy:", test_accuracy)
                predict_LR = pipe_LR.predict(X_test)
                if DEBUG: print(f"SVC => prediction::{predict_LR}")
                if DEBUG: print("-"*30)
                if DEBUG: print(f"SVC => accuracy score::{accuracy_score(y_test,predict_LR)}")
                if DEBUG: print("++++SVC",classification_report(y_test,predict_LR))
                joblib.dump(model, file_path)
                if DEBUG: print("-"*30)
                if DEBUG: print(f"Saved: {file_path}")
                if DEBUG: print("#"*20)

        else:
            if DEBUG: print("="*20)
            if DEBUG: print(f"model file exists===>{file_path}")
            if DEBUG: print("="*20)
            loaded_model = joblib.load(file_path)
            accuracy = loaded_model.score(X_test, y_test)
            if DEBUG: print(f"{file_path.split('_')[-1].split('.')[0]} Model accuracy: {accuracy}")
            if DEBUG: print("="*20)


subject_models = {
    'subject_model1_mnb': pipe_MNB,
    'subject_model2_cnb': pipe_CNB,
    'subject_model3_svc': pipe_SVC,
    'subject_model4_LR':  pipe_LR
}

save_folder = r'D:\\Desktop\\internship\\code\\saved_models'
os.makedirs(save_folder, exist_ok=True)




# Inside the function

def train_save_subject_models():
    for name, model in subject_models.items():
        file_path = os.path.join(save_folder, f'{name}.joblib')
        if not os.path.exists(file_path):
            if name =="subject_model1_mnb":
                if DEBUG: print("NOTE=======>Training the second model")
                pipe_MNB.fit(A_train,b_train)
                if DEBUG: print("NOTE=======>Training is finished")
                train_accuracy = model.score(A_train, b_train)
                test_accuracy = model.score(A_test, b_test)
                if DEBUG: print(f"{name} Train Accuracy:", train_accuracy)
                if DEBUG: print(f"{name} Test Accuracy:", test_accuracy)
                predict_MNB = pipe_MNB.predict(A_test)
                if DEBUG: print(f"MNB => prediction::{predict_MNB}")
                if DEBUG: print("-"*30)
                if DEBUG: print(f"MNB => accuracy score::{accuracy_score(b_test,predict_MNB)}")
                if DEBUG: print("++++MNB",classification_report(b_test,predict_MNB))
                joblib.dump(model, file_path)
                if DEBUG: print("-"*30)
                if DEBUG: print(f"Saved: {file_path}")
                if DEBUG: print("#"*20)

            if name =="subject_model2_cnb":
                if DEBUG: print("NOTE=======>Training the second model")
                pipe_CNB.fit(A_train,b_train)
                if DEBUG: print("NOTE=======>Training is finished")
                train_accuracy = model.score(A_train, b_train)
                test_accuracy = model.score(A_test, b_test)
                if DEBUG: print(f"{name} Train Accuracy:", train_accuracy)
                if DEBUG: print(f"{name} Test Accuracy:", test_accuracy)
                predict_CNB = pipe_CNB.predict(A_test)
                if DEBUG: print(f"CNB => prediction::{predict_CNB}")
                if DEBUG: print("-"*30)
                if DEBUG: print(f"CNB => accuracy score::{accuracy_score(b_test,predict_CNB)}")
                if DEBUG: print("++++CNB",classification_report(b_test,predict_CNB))
                joblib.dump(model, file_path)
                if DEBUG: print("-"*30)
                if DEBUG: print(f"Saved: {file_path}")
                if DEBUG: print("#"*20)

            if name =="subject_model3_svc":
                if DEBUG: print("NOTE=======>Training the second model")
                pipe_SVC.fit(A_train,b_train)
                if DEBUG: print("NOTE=======>Training is finished")
                train_accuracy = model.score(A_train, b_train)
                test_accuracy = model.score(A_test, b_test)
                if DEBUG: print(f"{name} Train Accuracy:", train_accuracy)
                if DEBUG: print(f"{name} Test Accuracy:", test_accuracy)
                predict_SVC = pipe_SVC.predict(A_test)
                if DEBUG: print(f"SVC => prediction::{predict_SVC}")
                if DEBUG: print("-"*30)
                if DEBUG: print(f"SVC => accuracy score::{accuracy_score(b_test,predict_SVC)}")
                if DEBUG: print("++++SVC",classification_report(b_test,predict_SVC))
                joblib.dump(model, file_path)
                if DEBUG: print("-"*30)
                if DEBUG: print(f"Saved: {file_path}")
                if DEBUG: print("#"*20)

            elif name =="subject_model4_LR":
                if DEBUG: print("NOTE=======>Training the model")
                pipe_LR.fit(A_train,b_train)
                if DEBUG: print("NOTE=======>Training is finished")
                train_accuracy = model.score(A_train, b_train)
                test_accuracy = model.score(A_test, b_test)
                if DEBUG: print(f"{name} Train Accuracy:", train_accuracy)
                if DEBUG: print(f"{name} Test Accuracy:", test_accuracy)
                predict_LR = pipe_LR.predict(A_test)
                if DEBUG: print(f"SVC => prediction::{predict_LR}")
                if DEBUG: print("-"*30)
                if DEBUG: print(f"SVC => accuracy score::{accuracy_score(b_test,predict_LR)}")
                if DEBUG: print("++++SVC",classification_report(b_test,predict_LR))
                joblib.dump(model, file_path)
                if DEBUG: print("-"*30)
                if DEBUG: print(f"Saved: {file_path}")
                if DEBUG: print("#"*20)

        else:
            if DEBUG: print("="*20)
            if DEBUG: print(f"model file exists===>{file_path}")
            if DEBUG: print("="*20)
            loaded_model = joblib.load(file_path)
            accuracy = loaded_model.score(X_test, y_test)
            if DEBUG: print(f"{file_path.split('_')[-1].split('.')[0]} Model accuracy: {accuracy}")


def test_model(email,model_file):
    try:
            spam_classifier = joblib.load(model_file)
            prediction = spam_classifier.predict(email)[0]
            if prediction == 1:
                result = colored("PHISHING", "red", attrs=["bold"])
                return True, result
            else:
                result = colored("SAFE", "light_green", attrs=["bold"])
                return False, result
    except Exception as e:
            with open("error.log", "a") as f:
                f.write(f"[ERROR] Failed to load {model_file}: {e}\n")
# testing emails
testing_emails = [
      """
    Hi sam,\n
        We detected a suspicious login attempt on your Outlook account from a new device in Casablanca, Morocco.\n
        Time: May 7, 2025 – 10:17 AM GMT+1\n
        Device: Chrome browser, Windows 10\n
        IP Address: 196.200.20.167\n
        If this was you, no action is required.\n
        If not, we strongly recommend you secure your account immediately to avoid unauthorized access.\n
        👉 https://securemyaccount-micros0ft.com\n
        This link will expire in 30 minutes.\n
        Thanks for helping keep your account safe.\n
        Outlook Security Team\n
        Microsoft Corporation\n

      """,
      """
      Dear User,\n
        We have detected unusual activity on your Microsoft account.\n 
        For your protection, your access will be temporarily disabled unless you verify your identity.\n
        Please confirm your account ownership by clicking the link below:\n
        👉 [Verify Now](http://micr0soft-support.com/secure-login)\n
        If you do not respond within 24 hours, your account will be locked permanently and all data may be lost.\n
        Thank you for your prompt attention to this matter.\n
        Sincerely,\n  
        Microsoft Security Team  
      """,
    "Thank you Mr Hamid for you time and your help \nSam Thomas",
    "Hello thank you for your help",
    "Congratulations! You've won $1,000,000. Click here to claim your prize!",
    "Meeting scheduled for tomorrow at 2pm, please confirm your attendance"
]

malicious_subjects = [
    "Your account will be suspended - Action required!",
    "URGENT: Security Alert from Bank of America",
    "Your tax refund is ready - Claim now!",
    "Congratulations! You've won a new iPhone",
    "Claim your $500 gift card now"]

train_save_subject_models()
train_save_body_models()


def test_emails(email,subject,links,sender_email):
    for model_file1,model_file2 in zip(body_models.keys(),subject_models.keys()):
        model_file1 = os.path.join(save_folder,f"{model_file1}.joblib")
        model_file2 = os.path.join(save_folder,f"{model_file2}.joblib")
        if DEBUG:
            print(colored(model_file1, "yellow", attrs=["bold"]))
            print("EMAIL MESSAGE:",colored(email, "blue", attrs=["bold"]))
        status1,result1 = test_model([email],model_file1)
        if DEBUG:
            print(f"Result: {result1}")
            print(colored(model_file2, "yellow", attrs=["bold"]))
            print("email subject:",colored(subject, "green", attrs=["bold"]))
        status2,result2 = test_model([subject],model_file2)
        if DEBUG: print(f"Result: {result2}")
         ###send notif only if email msg and subject are malicious and using one model
        print("importing funcs")
        from url_scanner import scan_url
        from email_scanner import check_email
        
        #check if one link is malicious and store it
        is_malicious_list = []
        if DEBUG:
             debug=True
        for link in links:
             is_malicious1=scan_url(link,debug=debug)
             if is_malicious1:
                  is_malicious_list.append(is_malicious1)

        pattern = r'<([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>'
        ex_sender_email = re.findall(pattern, sender_email)
        
        is_malicious2=check_email(ex_sender_email[0])
        if DEBUG:
             print(f"is email:{sender_email} malicious:{is_malicious2}")
        if all([status1,status2,is_malicious2]) and any(is_malicious_list) and all([model_file1=="model3_svc",model_file2=="subject_model3_svc"]): #if email is phishy
            from winotify import Notification, audio
            battery_low_alert = Notification('Email Scanner', 'ALERT',
                                            f"SUBJECT:{subject}\nMessage:{email[:10]}", 'D:\\Desktop\\internship\\code\\email_notif_icon.png', 'long')

            battery_low_alert.set_audio(audio.Default, loop=False)
            # showing toast message
            battery_low_alert.show()
            sys.exit(0)
        else:
            from winotify import Notification, audio

            battery_low_alert = Notification('Email Scanner', 'TEST ALERT',
                                            f"SUBJECT:{subject}\nMessage:{email[:10]}", 'D:\\Desktop\\internship\\code\\email.png', 'long')

            battery_low_alert.set_audio(audio.Default, loop=False)
            # showing toast message
            battery_low_alert.show()
            sys.exit(0)


#TODO
#1)optimize subject classfier  dataset | hyper params tf idf and classifer
#2)sender domain names,links, attachemtents scanning
#4) testing bert 
#https://medium.com/@maleeshadesilva21/text-classification-using-bert-an-complete-guide-7be30a8285c2
#https://github.com/charles9n/bert-sklearn
#https://medium.com/@khang.pham.exxact/text-classification-with-bert-7afaacc5e49b#




#NOTE ML ERRORS
# Signal, noise, and how they relate to overfitting.
# Goodness of fit from statistics
# Underfitting vs. overfitting
# The bias-variance tradeoff
# How to detect overfitting using train-test splits
# How to prevent overfitting using cross-validation, feature selection, regularization, etc
