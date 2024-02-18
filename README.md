Type `py api_client.py` into the terminal to run the program :)
Beware! It takes data from your camera! And make sure not to hurt yourself falling, have fun!
https://youtu.be/lxDbjzwF7sI?si=eYElnzT3ymtK4qDq

# Problem Space
Our team member has a personal connection to senior care in hospitals. Her loved one was sent to the hospital for a simple injury diagnosis, but his stay was extended due to a fall injury. Witnessing how devastating a simple fall could be, prolonging hospital stay by months, was eye-opening and served as the inspiration behind this project. In building this hack, our goal was to reduce the impact of fall injuries on senior health.

Every year in the US, between 700,000 and 1,000,000 hospital patients experience falls, resulting in approximately 250,000 injuries and up to 11,000 deaths. Shockingly, one in four falls leads to injury, with 10% causing serious harm such as fractures, lacerations, or internal bleeding. This greatly extrapolates to senior citizens who are already fragile. These incidents not only compromise patient well-being but also incur significant additional costs and prolonged hospital stays, diverting resources from addressing patients' primary medical concerns. Compounding the issue, limited hospital personnel creates struggle to effectively monitor each patient continuously. Consequently, patients may remain unattended after a fall, exacerbating their injuries. 

Clearly, there's a pressing need for innovative solutions to enhance senior patient safety and optimize hospital resources.


# Existing Solution/Competition
## 1. Camera/Sensor with Fall Detection
- Costs $50
- The average hospital has 2,000 - 3,000 cameras
- One time cost of $150,000 for replacements + installation fee

## 2. Alarm Systems (i.e. Pressure mats, infrared movement detectors, cord-activated alarms, wearable devices)
- Alarms are disruptive and may be especially disturbing to cognitively impaired patients, contributing to confusion and agitation. They also restrict mobility and independence; in US nursing homes, alarms are considered a type of restraint.

## 3. Sitters
- According to HospitalView, the average number of total staffed beds for hospitals is 130 beds
- To hire 130 sitters and pay them hourly is going to be very costly


## Our Solution
- Fall detection API for $15,000 annual subscription for our API service (revenue from one patient covers our API service for one year)
- Analyzes security camera footages at hospitals, provides instant alerts to the nearest hospital staff (through a pager or SMS) when a patient falls

## Impact
- Efficient Response: Hospital workers can attend to patients faster, minimizing response time
- Enhanced Patient Safety: Early detection and prompt assistance prevent exacerbation of existing injuries and reduce the risk of further injuries
- Hospital Efficiency: Optimizes resource allocation and streamlines patient care processes


# Market
The U.S. hospital facilities market size was valued at USD 1,411.7 billion in 2022 and is expected to grow at a compound annual growth rate (CAGR) of 7.7% from 2023 to 2030. 
According to American Hospital Association, there are 6,120 hospitals in the US
→ Total Available Market
According to the U.S. Department of Health & Human Services, ~20% of the hospitals are critically understaffed
→ Serviceable Available Market

# Business Model
API licensing sold at $15,000 per year
Revenue = 15000 x 6120(0.20) = $1.8 million per year


# Development Process
The dev process comprised of three main parts: 1. Model Training, 2. Model Deployment, and 3. User Experience. 

For model training, our approach was to develop a data preprocessing pipeline which prepared data before sending it to our training function to train our deep learning model. The preprocessing was crucial as it separates incoming video into batches of 60 frames, resizes each non-null image to be consistent with each other, normalizes its pixel values to a range between 0 and 1, adds it to a list, and then converts this list into a NumPy array. We also implemented data augmentation to quadruple the amount of video we had to train the model. This processed data was used to train our sequential architecture based convolutional LSTM model for the binary classification of "fall detected" and "no fall detected". For improved accuracy and reliability, we employed time-distributed convolutional layers to extract spatial features from each frame, and an LSTM layer to analyze temporal relationships between frames. Furthermore, we were able to overcome a problem of initial overfitting by introducing dropout layers in our model construction, as well as shuffling the indices of the video frames to ensure the model is trained on a randomized dataset, which helped improve generalization.

Deploying the model was necessary to implement it into a usable product interface for future customers and healthcare practitioners. After training, the model and its weights were saved as a ".keras" file allowing the model to be exported. Once a connection to a live video feed was established, we would invoke the pre-processing pipeline for the incoming data and then feed it to the ML model for detection of falls.

Finally, the user experience portion covered how our users would interact with and use our model. We interfaced with our laptop camera to simulate security cameras and enable a live video stream that got fed into our pre-processing and detection pipeline. When a fall was detected by our pre-trained model, an automatic SMS message using Sinch gets sent to nurse and doctor pagers/phones alerting them that a patient has fallen along with their fall location. 

# Next Steps
## 1. Enhanced Detection
Detect other behaviors besides falling, such as:
- Bed exit
- Restless in bed
- Room & toilet exit

## 2. Scaling and Expansion
Expand our audience to assisted living facilities such as:
- Nursing/retirement homes
- Rehab centers
