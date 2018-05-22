//
//  ProductModel.swift
//  ConditionsController
//
//  Created by olderor on 22.05.2018.
//  Copyright © 2018 Bohdan Yevchenko. All rights reserved.
//

import ObjectMapper

class ProductModel: ErrorModel {
  var id: Int!
  var name: String!
  var organizationId: Int!
  var trackingDeviceId: Int!
  var productTypeId: Int!
  var statusEn: String!
  var status: String!
  var dateCreated: String!
  var organizationName: String!
  var productTypeName: String!
  var trackingStatuses: [TrackingStatusModel]!
  var conditions: [ConditionModel]!
  
  required init?(map: Map){
    super.init(map: map)
  }
  
  override func mapping(map: Map) {
    super.mapping(map: map)
    
    id <- map["product.id"]
    name <- map["product.name"]
    organizationId <- map["product.organization_id"]
    trackingDeviceId <- map["product.tracking_device_id"]
    productTypeId <- map["product.product_type_id"]
    statusEn <- map["product.status_en"]
    status <- map["product.status"]
    dateCreated <- map["product.date_created"]
    organizationName <- map["product.organization_name"]
    productTypeName <- map["product.product_type_name"]
    trackingStatuses <- map["product.tracking_statuses"]
    conditions <- map["product.conditions"]
  }
}
