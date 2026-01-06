# Automated Image Resizing Using AWS S3, Lambda & SNS

This project implements an event-driven serverless workflow where images uploaded to a **source S3 bucket** are automatically resized using an AWS Lambda function. The resized images are stored in a **destination S3 bucket**, and a notification email is sent via **Amazon SNS**.

This setup is useful in real-world scenarios such as:

* Generating thumbnails
* Preparing compressed images for web delivery
* Optimizing storage costs by resizing images on upload
* Automating media processing pipelines

---

## Architecture Overview

When a user uploads an image to the source bucket:

1. S3 triggers the Lambda function
2. Lambda reads the image from **Bucket-1**
3. Image is resized using Pillow (PIL library)
4. Resized image is stored in **Bucket-2**
5. SNS sends an email notification

This ensures the entire process is:

* **Fully automated**
* **Serverless (no servers to manage)**
* **Scalable on demand**
* **Cost-efficient**

---

## Resource & Variable Naming (Fill these before deployment)

Use this section to define your resource names.

| Variable               | Description                         | Your Value |
| ---------------------- | ----------------------------------- | ---------- |
| `BUCKET_1_NAME`        | Source bucket (original images)     |    non-resized-image-bucket-123        |
| `BUCKET_2_NAME`        | Destination bucket (resized images) |     resized-image-bbucket-123       |
| `AWS_REGION`           | Region where resources are created  |        ap-south-1    |
| `SNS_TOPIC_NAME`       | SNS topic for notifications         |    resize-image-sns-topic        |
| `NOTIFICATION_EMAIL`   | Email ID to receive alerts          |    xyz.com        |
| `LAMBDA_FUNCTION_NAME` | Name of Lambda function             |       resize-image-lambda-function     |
| `LAMBDA_HANDLER_NAME`  | Handler (file.function)             |    lambda_function.handler        |
| `DEST_BUCKET_ENV_KEY`  | Env variable key for bucket name    |      arn:aws:sns****      |
| `SNS_TOPIC_ENV_KEY`    | Env variable key for SNS ARN        |      resized-image-bbucket-123      |

---

## Prerequisites

You should have:

* An AWS account with required permissions
* Basic understanding of:

  * S3
  * Lambda
  * IAM
  * SNS

---

## Step 1 — Create Two S3 Buckets (Source & Destination)

We create two separate buckets because:

✔ The first bucket stores **original images**
✔ The second bucket stores **processed / resized images**
✔ This separation ensures clarity, security & lifecycle management

### Actions

1. Go to **AWS S3 Console → Create bucket**
2. Enter the name for **Bucket-1 (Source)**

Fill your value:

```
BUCKET_1_NAME = non-resized-image-bucket-123
```

Click **Create bucket**

3. Repeat the same process to create **Bucket-2 (Destination)**

```
BUCKET_2_NAME = resized-image-bucket-123
```

Once created, we have:

* Bucket-1 → Upload images here
* Bucket-2 → Resized images will be stored here

<img width="1912" height="426" alt="image" src="https://github.com/user-attachments/assets/fec5a287-c368-4a14-8270-bbc161a3db5b" />

---

## Step 2 — Create SNS Topic & Email Subscription

SNS will notify us whenever an image is resized.

We use SNS because:

✔ It decouples notification handling
✔ Supports multiple subscribers (email, webhook, etc.)
✔ Provides delivery reliability

### 🔹 Actions

1. Open **SNS Console → Topics → Create topic**
2. Select **Standard**
3. Enter topic name:

```
SNS_TOPIC_NAME = resize-image-sns-topic
```
<img width="2404" height="466" alt="image" src="https://github.com/user-attachments/assets/7b01d5f5-7915-44a7-ba42-79dc36ddebd9" />

Create topic.

4. Click **Create Subscription**
5. Select:

* Protocol → `Email`
* Endpoint →

```
NOTIFICATION_EMAIL = xyz.com
```
<img width="2880" height="850" alt="image" src="https://github.com/user-attachments/assets/3bde2f35-6d00-4f42-8f77-1bc12bf37087" />

6. Check your inbox & click **Confirm Subscription**

Status should change:

```
Pending → Confirmed
```
<img width="1088" height="256" alt="image" src="https://github.com/user-attachments/assets/638124c5-feac-42e5-8c1e-e74a35d608f4" />

---

## Step 3 — Create Lambda Function

This Lambda function performs image resizing.

We use Lambda because:

✔ It runs only when triggered
✔ No server management required
✔ Highly scalable
✔ Cost efficient for event-driven workloads

### 🔹 Actions

1. Go to **Lambda Console → Create Function**
2. Enter:

```
LAMBDA_FUNCTION_NAME =  resize-image-lambda-function
Runtime = Python 3.9
Execution role = Create new role with basic permissions
```

<img width="2940" height="1456" alt="image" src="https://github.com/user-attachments/assets/ff4ade93-8ba5-4980-bfee-cca7074d746b" />

Click **Create Function**

---

## Step 4 — Add Lambda Code

Replace default code with your resize function. 
Check lambda_function.py file in this github repo

Click **Deploy**

> The code should:
>
> * Read object from S3 event
> * Resize image using Pillow
> * Upload to destination bucket
> * Publish SNS notification

---

## Step 5 — Configure Runtime Handler

Handler tells Lambda **which file & function to execute**.

Example:

```
LAMBDA_HANDLER_NAME = lambda_function.handler
```

<img width="2940" height="1196" alt="image" src="https://github.com/user-attachments/assets/3dd40901-2c2e-4ce4-a238-e77b70604e44" />

Go to:

`Code → Runtime settings → Edit`

Enter handler name → Save

---

## Step 6 — Add Environment Variables

Instead of hard-coding values in code,
we store them in environment variables for flexibility & portability.

Go to:

`Configuration → Environment Variables → Edit`

Add:

| Key                                | Value           |
| ---------------------------------- | --------------- |
| `DEST_BUCKET_ENV_KEY = <key name>` | arn:aws:**** |
| `SNS_TOPIC_ENV_KEY = <key name>`   | resized-image-bucket-123 |

This allows easy modification without changing code.


<img width="2918" height="746" alt="image" src="https://github.com/user-attachments/assets/3707e170-bbd0-4248-9a03-0fe600340a27" />

---

## Step 7 — Increase Timeout & Memory

Image resizing requires adequate compute resources.

We increase these to avoid failures due to:

* Large images
* High processing time
* Memory buffering

Go to:

`Configuration → General configuration → Edit`

Set:

```
Timeout = 1 minute
Memory = 256 MB
```

Save.

<img width="2390" height="340" alt="image" src="https://github.com/user-attachments/assets/6070daf6-ee8e-433c-b6f4-0bcf64352deb" />

---

## Step 8 — Add Pillow (PIL) Lambda Layer

Pillow is required for image processing.

We add a Lambda Layer instead of packaging dependencies because:

✔ Reduces deployment package size
✔ Improves performance
✔ Easier dependency management

Add layer ARN:

```
arn:aws:lambda:ap-south-1:770693421928:layer:Klayers-p310-Pillow:13
```

Save.

You can finf the choice of your arn here:
```
https://github.com/keithrozario/Klayers/tree/master/deployments/python3.10
```

---

## Step 9 — Configure IAM Permissions

Lambda needs explicit permissions to:

* Read objects from Bucket-1
* Write resized image to Bucket-2
* Publish SNS messages

Open:

`IAM → Roles → Select Lambda Execution Role`

Attach:

* `AmazonS3FullAccess`
* `AmazonSNSFullAccess`

<img width="2330" height="642" alt="image" src="https://github.com/user-attachments/assets/2be9c4f3-9846-4d1d-9cab-35743187ed32" />

---

## Step 10 — Add S3 Trigger (Event-Driven Execution)

We configure Bucket-1 to trigger Lambda on image upload.

This ensures:

✔ No manual execution
✔ Real-time processing
✔ Event-driven architecture

Go to Lambda → Triggers → Add Trigger

Select:

```
Source = S3
Bucket = non-resized-image-bucket-123
Event Type = ObjectCreated:Put
```

Add trigger.

<img width="2940" height="1530" alt="image" src="https://github.com/user-attachments/assets/99cbd8c2-65d1-402d-9617-93241feb24ca" />

Then, Add a new test event, change the name of bucket i.e. first bucket, arn i.e. first bucket arn and object key

<img width="1942" height="1382" alt="image" src="https://github.com/user-attachments/assets/c4813675-74da-4a5b-abd0-5bdbcd2cae65" />

---

## Step 11 — Test the Workflow

Upload an image to:

```
non-resized-bucket-image-123 (Source)
```

<img width="2940" height="702" alt="image" src="https://github.com/user-attachments/assets/8c7b45a6-f2c2-47fa-b219-1968e979ed24" />

Expected results:

✔ Lambda resizes image
✔ Resized image appears in Bucket-2

<img width="2940" height="702" alt="image" src="https://github.com/user-attachments/assets/50fb8ce0-2796-44b1-899a-80e0797d0d97" />

✔ File size is reduced
✔ Email notification is received

<img width="2940" height="702" alt="image" src="https://github.com/user-attachments/assets/e6ef58ee-9930-47dc-b159-0985254e5019" />

Example:

| File     | Size   |
| -------- | ------ |
| Original | 38.4 KB |
| Resized  | 11.2 KB |

---

## Optional Cleanup

To avoid costs, delete:

* Lambda function
* SNS topic
* IAM role
* S3 buckets

---

## Troubleshooting — Runtime.ImportModule Error (Handler Name Mismatch)

During testing, I encountered the following Lambda runtime error:

```
Runtime.ImportModuleError: Unable to import module 'CreateThumbnail':
No module named 'CreateThumbnail'
```

<img width="2316" height="1184" alt="image" src="https://github.com/user-attachments/assets/07b7f7ef-f078-4d91-ac53-270bf0d3330c" />

### Why This Error Occurred

Lambda could not find the Python file specified in the **Handler setting**.

I had configured the handler as:

```
CreateThumbnail.handler
```

However, when I checked the CloudWatch logs, I discovered that my actual Python file name was:

```
lambda_function.py
```

This meant Lambda was trying to import a module that did not exist.

---

### Root Cause

The handler format in Lambda is:

```
<python_filename>.<function_name>
```

Since my file name was `lambda_function.py`, the correct handler should be:

```
lambda_function.handler
```

---

### Fix Applied

1️⃣ I opened:

```
Lambda Console → Configuration → Runtime Settings → Edit
```

2️⃣ I updated the handler value to:

```
lambda_function.handler
```

3️⃣ Clicked **Save**, then redeployed the function.

---

### Result

After correcting the handler:

✔ Lambda successfully imported the function
✔ Image resizing started working
✔ Resized images were stored in Bucket-2
✔ SNS email notification was received

Everything worked as expected.

---

### Takeaway

Always verify:

* Python file name in Lambda
* Handler configuration format
* CloudWatch logs for debugging

CloudWatch provided the exact clue that helped resolve this issue.
