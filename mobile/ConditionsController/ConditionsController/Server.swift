//
//  Server.swift
//  ConditionsController
//
//  Created by olderor on 21.05.2018.
//  Copyright © 2018 Bohdan Yevchenko. All rights reserved.
//

import Foundation
import Alamofire
import AlamofireObjectMapper

class Server
{
  static let url = "https://conditions-controller-olderor.c9users.io/api/"
  
  enum Action : String {
    case getProductInfo        = "product/get"
    case getProductTrackings        = "product/get-tracks"
  }
  
  static func getProductInfo(productId: String, onSuccess: @escaping (_ product: ProductModel?) -> ()) {
    let uri = url + Action.getProductInfo.rawValue
    let params = ["product_id": productId]
    Alamofire.request(uri, method: .post, parameters: params, encoding: JSONEncoding.default, headers: nil)
      .responseObject { (response: DataResponse<ProductModel>) in
        onSuccess(response.result.value)
    }
  }
  
  static func getProductTrackings(productId: String, fromDate: String?, onSuccess: @escaping (_ product: ProductModel?) -> ()) {
    let uri = url + Action.getProductTrackings.rawValue
    let params = ["product_id": productId, "from_date": fromDate ?? ""]
    Alamofire.request(uri, method: .post, parameters: params, encoding: JSONEncoding.default, headers: nil)
      .responseObject { (response: DataResponse<ProductModel>) in
        onSuccess(response.result.value)
    }
  }
}
