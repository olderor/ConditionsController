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
  static let url = "https://127.0.0.1:5002/api/"
  
  enum Action : String {
    case getProductInfo        = "product/get"
  }
  
  static func getProductInfo(productId: String, onSuccess: @escaping (_ product: ProductModel?) -> ()) {
    let uri = url + Action.getProductInfo.rawValue
    let params = ["product_id": productId]
    Alamofire.request(uri, method: .post, parameters: params, encoding: JSONEncoding.default, headers: nil)
      .responseObject(keyPath: "product") { (response: DataResponse<ProductModel>) in
        onSuccess(response.result.value)
    }
  }
}