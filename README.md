# supermarket-aggregator

Developing a supermarket aggregator to check and compare prices of different products from different supermarkets.


I am creating a supermarket aggregator that has the following steps:

1 - collects data from website and sends data to queu.
2 - another process reads qeue and updates db.
3 - There is an api that reads db and returns data.
4 - Front end that makes requests to api.

This needs to be free tier only as much as possible and on AWS and also thorugh terraform code.

Some considerations.
- step one takes about five minutes.
- It gathers products from five supermakets.
- Each supermarket has fifty thousand products.
- Right now it is only Portugal supermarkets but needs to be scalable to other countries.

Can you help with some questions?
 - Let me know if this is a good architecture and if it is scalable enough?
 - Can you help me with the implementation? What are the best practices, which tools to use and how can I implement it?
 - Can you pre define some price tiers, including a free tier? For example, a free, lite, premium and dev tier.
 - What should be included with each tier?
 - Can you help me with how should I integrate ads?
 - Can you help me with how should I integrate subscriptions and payments?


# Supermarket Aggregator Architecture

## Overview
Collect product prices from multiple supermarkets, provide API for apps, support subscriptions, and store price history.

## AWS Services
| Step | Functionality | AWS Service | Notes |
|------|---------------|------------|-------|
| 1 | Scraper collects product data | Lambda + EventBridge | Important products daily, less important every 2-3 days |
| 2 | Queue data | SQS | Decouples scraper & DB |
| 3 | Process queue & update DB | Lambda + DynamoDB | Two tables: Products & Prices |
| 4 | Provide API | API Gateway + Lambda | Frontend, mobile, developer API tier |
| 5 | Frontend | S3 + CloudFront | Static frontend |
| 6 | Subscription & payments | Stripe | Lite/Premium/Dev subscriptions |
| 7 | Logging | CloudWatch | Monitor Lambda executions, API, DB |

## Data Model
**Products Table:** product_id (PK), name, category, brand  
**Prices Table:** price_id (PK), product_id (FK), supermarket_id, price, timestamp  

## Subscription Tiers
| Tier | Features |
|------|---------|
| Free | Basic search, limited API, ads |
| Lite | Fewer ads, favorites, price history |
| Premium | Full features, price alerts |
| Dev | 1 API key, developer access |


## Implementation Steps
1. Scraper Lambda → EventBridge → SQS  
2. Queue Processing Lambda → Update DynamoDB  
3. DynamoDB Tables → Products & Prices  
4. API Gateway + Lambda → Endpoints: /search, /price-history, /favorites, /subscriptions  
5. Frontend → React/Vue SPA on S3 + CloudFront  
6. Stripe → Handle subscriptions and VAT  
7. CloudWatch → Logs & metrics  

## Scaling Notes
- DynamoDB serverless → auto-scaling  
- SQS decouples scraping & DB updates  
- Lambda + API Gateway → handle bursts  
- Estimated costs: AWS €55/month + domain €1.33/month
