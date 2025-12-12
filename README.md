
# Setup instructions 
## Quick Setup

### macOS / Linux
```bash
python3 -m venv .venv \
&& source .venv/bin/activate \
&& pip install --upgrade pip \
&& pip install -r requirements.txt
```
Install awscli and configure your environment:
```bash
brew install awscli
&& aws configure
```
Verify installation:
```bash
aws sts get-caller-identity
```

# Documentation 
# practical examples illustrating the system's results

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
