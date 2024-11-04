# Database Schema for Order Management System

## Overview

This database schema represents an Order Management System, where `Orders` serves as the main table, encapsulating essential information about each order and its associated details. The design follows a normalized approach with separate tables for different aspects like COD, Confirmation, Address, Receiver, Star, and Tracker.

## Table Descriptions

### 1. `Orders` Table
The `Orders` table is the primary table representing an order. It contains attributes such as:
- `_id`: Unique identifier for the order.
- `order_id`: Secondary identifier for tracking the order.
- `type`: Type of order (e.g., SEND).
- `createdAt`: Date and time when the order was created.
- `updatedAt`: Date and time when the order was last updated.
- `collectedFromBusiness`: Date and time of a payment collection from the business.
- Foreign Key References:
  - `confirmation_id`: Links to the `Confirmation` table.
  - `dropOffAddress_id`: Links to the `Address` table for the drop-off address.
  - `pickupAddress_id`: Links to the `Address` table for the pickup address.
  - `receiver_id`: Links to the `Receiver` table.
  - `star_id`: Links to the `Star` table.
  - `tracker_id`: Links to the `Tracker` table.
  - `cod_id`: Links to the `COD` table.

### 2. `COD` Table
The `COD` (Cash on Delivery) table contains details about payment collection, including:
- `_id`: Unique identifier for the COD entry.
- `amount`: The COD amount due.
- `isPaidBack`: Indicates if the COD amount was paid back to the business (boolean).
- `collectedAmount`: The amount collected for the COD.

### 3. `Confirmation` Table
The `Confirmation` table holds details related to order confirmation, including:
- `_id`: Unique identifier for the confirmation.
- `isConfirmed`: Indicates whether the order is confirmed (boolean).
- `numberOfSmsTrials`: Number of SMS attempts for confirmation.

### 4. `Address` Table
The `Address` table is used for both drop-off and pickup addresses associated with an order. It includes:
- `_id`: Unique identifier for the address.
- `floor`: Floor number in the address.
- `apartment`: Apartment or suite number.
- `secondLine`: Additional address details.
- `district`: District or neighborhood name.
- `firstLine`: Primary address line.
- `geoLocation_lat` and `geoLocation_long`: Geographic coordinates (latitude and longitude).
- Foreign Key References:
  - `city_id`: Links to the `City` table.
  - `zone_id`: Links to the `Zone` table.
  - `country_id`: Links to the `Country` table.

### 5. `City` Table
The `City` table stores city information associated with addresses. It contains:
- `_id`: Unique identifier for the city.
- `name`: Name of the city.

### 6. `Zone` Table
The `Zone` table represents zones within a city. It contains:
- `_id`: Unique identifier for the zone.
- `name`: Name of the zone.

### 7. `Country` Table
The `Country` table stores country information for addresses. It includes:
- `_id`: Unique identifier for the country.
- `name`: Name of the country.
- `code`: Country code (e.g., "EG" for Egypt).

### 8. `Receiver` Table
The `Receiver` table contains information about the recipient of the order. It includes:
- `_id`: Unique identifier for the receiver.
- `firstName`: Receiver's first name.
- `lastName`: Receiver's last name.
- `phone`: Receiver's phone number.

### 9. `Star` Table
The `Star` table stores additional contact information related to the order. It includes:
- `_id`: Unique identifier for the contact.
- `name`: Name of the contact.
- `phone`: Contact's phone number.

### 10. `Tracker` Table
The `Tracker` table contains tracking information for the order. It includes:
- `_id`: Unique identifier for the tracker entry.
- `trackerId`: Tracker ID for the order.
- `order_id`: Order identifier linked with tracking.

## Entity-Relationship Overview

- **Orders** is the main entity, representing the core details of an order, including references to several related entities.
- **COD**: Linked to an order to represent payment collection details for Cash on Delivery.
- **Confirmation**: Linked to an order to represent its confirmation details.
- **Address**: Used for both drop-off and pickup locations. Contains references to `City`, `Zone`, and `Country` for normalized address information.
- **Receiver**: Represents the recipient of the order.
- **Star**: Additional contact associated with the order.
- **Tracker**: Tracks the order’s status and progress.

## Indexes
In this schema, several indexes have been added to optimize query performance. 
The `Orders` table includes indexes on the `order_id` and `type` columns. 
These indexes are designed to improve the efficiency of queries that frequently filter or search based on `order_id` (e.g., retrieving specific orders by their unique identifier) or `type` (e.g., filtering orders by type category). In the `City`, `Zone`, and `Country` tables, indexes on the `name` column have been added. 
These indexes allow for faster lookups when searching by name, which is useful for queries that involve location-based filtering or reporting. 
Overall, these indexes help speed up data retrieval by allowing the database to locate rows more quickly, reducing the time complexity of search operations on large datasets.

## Summary

This schema is designed to facilitate efficient storage, retrieval, and management of order-related information in a relational database. The normalized structure minimizes redundancy and enhances scalability, making it suitable for complex order management operations with multiple associated details.