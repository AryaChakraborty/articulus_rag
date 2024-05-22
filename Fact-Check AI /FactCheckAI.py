#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional, SpatialDropout1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


# In[2]:


# Load dataset
df = pd.read_json("C:\\Users\\Shaurya\\Downloads\\Dataset\\politifact_factcheck_data.json", lines=True)


# In[3]:


# Clean text data
def clean_text(text):
    # Implement text cleaning here
    return text

df['cleaned_statement'] = df['statement'].apply(clean_text)

# Binarize labels
binary_map = {'true': 1, 'mostly-true': 1, 'half-true': 1, 'mostly-false': 0, 'false': 0, 'pants-fire': 0}
df['binary_verdict'] = df['verdict'].map(binary_map)

# Tokenization and Padding
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(df['cleaned_statement'])
sequences = tokenizer.texts_to_sequences(df['cleaned_statement'])
padded_sequences = pad_sequences(sequences, maxlen=200)


# In[4]:


# Model parameters
vocab_size = 5000  
embedding_dim = 64
max_length = 200 
trunc_type = 'post'
padding_type = 'post'


# In[5]:


# Build the model
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_length))
model.add(SpatialDropout1D(0.4))  # Increased dropout for regularization
model.add(Bidirectional(LSTM(64, dropout=0.3, recurrent_dropout=0.3)))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.4))  # Increased dropout for regularization
model.add(Dense(1, activation='sigmoid'))


# In[6]:


model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()


# In[7]:


# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, df['binary_verdict'], test_size=0.2)


# In[8]:


# Early stopping to prevent overfitting
early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Train the model
history = model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test), callbacks=[early_stop])


# In[9]:


# Evaluate the model
predictions = model.predict(X_test)
y_pred = [1 if p > 0.5 else 0 for p in predictions]

print("Accuracy: ", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


# In[11]:


# Plot training history
import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')


# In[ ]:




