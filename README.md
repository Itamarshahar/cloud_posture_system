# Setup instructions 

## macOS / Linux
```bash
python3 -m venv .venv \
&& source .venv/bin/activate \
&& python -m pip install --upgrade pip \
&& python -m pip install -r requirements.txt
```
Install awscli and configure your environment:
```bash
brew install awscli \
&& aws configure
```
Verify installation:
```bash
aws sts get-caller-identity
```
How to run:
```bash
python main.py --account_id <aws_account_id> --region <aws_region>
```

# Documentation
## Misconfigurations support:
The module performs a security posture analysis of AWS S3 buckets, detecting the following misconfigurations:
* S3 Bucket Default Encryption Disabled
* S3 Bucket Object Versioning Disabled
* S3 Bucket MFA Delete Not Enabled
* S3 Bucket Object Lock Disabled
## General structure:
The module is structured into several key components:


# practical examples illustrating the system's results


For example:
```bash
python main.py --account_id 12345678912 --region eu-central-1
```
The output will be:
```
================================================================================
Misconfiguration: S3 Bucket Default Encryption Disabled
Account: 123456789012 | Severity: HIGH | Status: PASSED
================================================================================
Description:
  S3 Bucket does not have default encryption enabled.

Remediation Steps:
  Enable default server-side encryption on the S3 bucket to ensure that all objects are encrypted at rest. Enforcing encryption strengthens data protection and helps meet security and compliance requirements. You can enable default encryption using the AWS CLI with the following command: aws s3api put-bucket-encryption --bucket <BUCKET_NAME> --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'. For additional guidance and best practices, refer to AWS documentation: https://aws.amazon.com/blogs/security/how-to-prevent-uploads-of-unencrypted-objects-to-amazon-s3/.

Affected Resources:
--------------------------------------------------------------------------------
Name                           Resource ID                              Status    
--------------------------------------------------------------------------------
itamar-bucket-2                arn:aws:s3:::itamar-bucket-2             PASSED    
not-encrypted-test             arn:aws:s3:::not-encrypted-test          PASSED    
--------------------------------------------------------------------------------


================================================================================
Misconfiguration: S3 Bucket Object Versioning Disabled
Account: 123456789012 | Severity: HIGH | Status: FAILED
================================================================================
Description:
  S3 Bucket does not have object versioning enabled.

Remediation Steps:
  Enable S3 bucket versioning to retain previous versions of objects and protect against accidental overwrites, deletions, and malicious modifications. Versioning is a foundational control for data recovery and ransomware resilience. You can enable versioning using the AWS Management Console or API. AWS guidance is available at: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html. 

Affected Resources:
--------------------------------------------------------------------------------
Name                           Resource ID                              Status    
--------------------------------------------------------------------------------
itamar-bucket-2                arn:aws:s3:::itamar-bucket-2             FAILED    
not-encrypted-test             arn:aws:s3:::not-encrypted-test          FAILED    
--------------------------------------------------------------------------------


================================================================================
Misconfiguration: S3 Bucket MFA Delete Not Enabled
Account: 123456789012 | Severity: MEDIUM | Status: FAILED
================================================================================
Description:
  S3 Bucket does not have MFA Delete enabled.

Remediation Steps:
  Enable MFA Delete on the S3 bucket to require multi-factor authentication when changing the bucket versioning state or deleting object versions. This adds an additional layer of protection against accidental or malicious data deletion in the event of compromised IAM credentials. You can enable MFA Delete using the AWS CLI (requires root or privileged credentials): aws s3api put-bucket-versioning --profile <ROOT_PROFILE> --bucket <BUCKET_NAME> --versioning-configuration Status=Enabled,MFADelete=Enabled --mfa 'arn:aws:iam::<ACCOUNT_ID>:mfa/<MFA_DEVICE> <MFA_CODE>'. For more details, see AWS documentation: https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiFactorAuthenticationDelete.html. 

Affected Resources:
--------------------------------------------------------------------------------
Name                           Resource ID                              Status    
--------------------------------------------------------------------------------
itamar-bucket-2                arn:aws:s3:::itamar-bucket-2             FAILED    
not-encrypted-test             arn:aws:s3:::not-encrypted-test          FAILED    
--------------------------------------------------------------------------------


================================================================================
Misconfiguration: S3 Bucket Object Lock Disabled
Account: 123456789012 | Severity: MEDIUM | Status: FAILED
================================================================================
Description:
  S3 Bucket does not have Object Lock enabled.

Remediation Steps:
  Enable S3 Object Lock on the bucket to enforce write-once-read-many (WORM) protections. Object Lock prevents objects from being deleted or overwritten for a defined retention period, strengthening protection against ransomware and unauthorized data tampering, especially for backups and audit logs. Object Lock can be enabled using the AWS CLI as follows: aws s3 put-object-lock-configuration --bucket <BUCKET_NAME> --object-lock-configuration '{"ObjectLockEnabled":"Enabled","Rule":{"DefaultRetention":{"Mode":"GOVERNANCE","Days":1}}}'. For more information, see AWS documentation: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html. 

Affected Resources:
--------------------------------------------------------------------------------
Name                           Resource ID                              Status    
--------------------------------------------------------------------------------
itamar-bucket-2                arn:aws:s3:::itamar-bucket-2             FAILED    
not-encrypted-test             arn:aws:s3:::not-encrypted-test          FAILED    
--------------------------------------------------------------------------------
```




# Cloud Posture Security Analysis for AWS S3
Amazon Simple Storage Service (S3) is a highly scalable object storage service designed for storing and retrieving unstructured data at any scale.
It is commonly used to host application assets, store backups and database exports, collect logs, and build data lakes. 
Core S3 assets include buckets (logical containers) and objects (stored files), along with configuration mechanisms such as bucket policies, access control lists (ACLs), Block Public Access, default encryption, versioning, logging, and Object Ownership controls.

From a security perspective, S3 is a high-value target because it often stores sensitive and business-critical data. Attackers are primarily interested in buckets that contain personally identifiable information (PII), credentials, backups, database exports, or operational logs that may reveal infrastructure details. Publicly accessible buckets are a frequent attack vector, especially when they unintentionally expose sensitive content.

Key areas of interest for attackers include misconfigured access controls, such as publicly accessible buckets or overly permissive bucket policies that allow cross-account or wildcard access. 
Additional targets include buckets without encryption at rest, which weakens defense-in-depth; buckets without logging, which limits detection and forensic capabilities; and buckets without versioning or protection mechanisms, making them vulnerable to destructive actions such as data deletion or ransomware-style overwrites.


# Common misconfigurations that could be exploited by attackers:
## Public Access Block Disabled - Severity: CRITICAL

### Description of the misconfiguration and risk
   S3 Block Public Access settings are not fully enabled, allowing buckets to become publicly accessible through bucket policies or ACLs. This misconfiguration can directly expose sensitive data to the public internet.

### Potential attack scenario or impact
An attacker discovers a publicly accessible bucket through internet scanning, leaked URLs, or misconfigured applications and downloads sensitive data such as backups, logs, or PII. If public write access is allowed, attackers may also upload malicious content or tamper with stored data.

### AWS best practice recommendation for remediation
Enable S3 Block Public Access at both the account and bucket levels and ensure that bucket policies do not allow public principals 
https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html

## Default Encryption Disabled (s3_bucket_default_encryption) - Severity: HIGH

### Description of the misconfiguration and risk
The bucket does not enforce server-side encryption by default, allowing objects to be stored unencrypted at rest. This weakens defense-in-depth and may violate regulatory or compliance requirements.

### Potential attack scenario or impact
If an attacker gains unauthorized access to stored data through misconfiguration or credential compromise, unencrypted objects increase the severity of data exposure and potential compliance impact.

### AWS best practice recommendation for remediation
Enable default encryption using SSE-S3 or SSE-KMS, and enforce encryption through a bucket policy that denies unencrypted uploads.
https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-bucket-encryption.html

## Object Versioning Disabled (s3_bucket_object_versioning) - Severity: HIGH

### Description of the misconfiguration and risk
S3 versioning is disabled, meaning object overwrites and deletions are permanent. This increases the risk of irreversible data loss due to accidental or malicious actions.

### Potential attack scenario or impact
An attacker with write or delete permissions can overwrite or delete objects, effectively causing data loss or simulating a ransomware-style attack with limited recovery options.

### AWS best practice recommendation for remediation
Enable S3 Versioning to preserve previous versions of objects and allow recovery from unintended or malicious changes.
https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html


## Object Lock Not Enabled (s3_bucket_object_lock) - Severity: MEDIUM

### Description of the misconfiguration and risk
Object Lock is not enabled, preventing the use of write-once-read-many (WORM) protections. This limits the ability to enforce immutability for critical data such as backups and audit logs.

### Potential attack scenario or impact
An attacker with sufficient permissions may delete or modify backup data, undermining recovery efforts following a security incident or ransomware attack.

### AWS best practice recommendation for remediation
Enable S3 Object Lock in Governance or Compliance mode for critical buckets to prevent deletion or modification of objects for a defined retention period.
https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html

## MFA Delete Disabled (s3_bucket_enable_mfa_delete) - Severity: MEDIUM

### Description of the misconfiguration and risk
MFA Delete is not enabled, allowing object deletions or versioning state changes without multi-factor authentication. This increases the impact of compromised credentials.

### Potential attack scenario or impact
If an attacker gains access to valid IAM credentials, they can permanently delete object versions or disable versioning, resulting in irreversible data loss and damge to the reliability.

### AWS best practice recommendation for remediation
Enable MFA Delete for highly sensitive buckets where operationally feasible, and restrict versioning and delete permissions to trusted principals only.
https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiFactorAuthenticationDelete.html


Ensure your repository includes both research findings and working code
You may use official AWS documentation, security best practices guides, and standard developer resources.
