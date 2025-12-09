# supermarket-aggregator
Developing a supermarket aggregator to check and compare prices of different products from different supermarkets.


I am creating a supermarket aggregator that has the following steps:

1 - collects data from website and sends data to queu.
2 - another process reads qeue and updates db. Needs to be realtional.
3 - There is an api that reads db and returns data.
4 - Front end that makes requests to api.

This needs to be free tier only. Compare solutions between azure, google cloud and aws. It could be multi cloud, if stays on free tier.

Some considerations. stepp one takes about five minutes.

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
