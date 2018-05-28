//
//  ViewController.swift
//  ConditionsController
//
//  Created by olderor on 21.05.2018.
//  Copyright © 2018 Bohdan Yevchenko. All rights reserved.
//


import UIKit
import AVFoundation

class QRScannerController: UIViewController {
  
  @IBOutlet var messageLabel:UILabel!
  @IBOutlet var topbar: UIView!
  
  var captureSession = AVCaptureSession()
  
  var videoPreviewLayer: AVCaptureVideoPreviewLayer?
  var qrCodeFrameView: UIView?
  var decodedData: String!
  var messageText: String!
  
  private let supportedCodeTypes = [AVMetadataObject.ObjectType.upce,
                                    AVMetadataObject.ObjectType.code39,
                                    AVMetadataObject.ObjectType.code39Mod43,
                                    AVMetadataObject.ObjectType.code93,
                                    AVMetadataObject.ObjectType.code128,
                                    AVMetadataObject.ObjectType.ean8,
                                    AVMetadataObject.ObjectType.ean13,
                                    AVMetadataObject.ObjectType.aztec,
                                    AVMetadataObject.ObjectType.pdf417,
                                    AVMetadataObject.ObjectType.itf14,
                                    AVMetadataObject.ObjectType.dataMatrix,
                                    AVMetadataObject.ObjectType.interleaved2of5,
                                    AVMetadataObject.ObjectType.qr]
  
  override func viewDidLoad() {
    super.viewDidLoad()
    messageText = messageLabel.text
    let captureDevice = AVCaptureDevice.default(for: AVMediaType.video)
    
    do {
      let input = try AVCaptureDeviceInput(device: captureDevice!)
      
      captureSession.addInput(input)
      
      let captureMetadataOutput = AVCaptureMetadataOutput()
      captureSession.addOutput(captureMetadataOutput)
      
      captureMetadataOutput.setMetadataObjectsDelegate(self, queue: DispatchQueue.main)
      captureMetadataOutput.metadataObjectTypes = supportedCodeTypes
      
    } catch {
      print(error)
      return
    }
    
    videoPreviewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
    videoPreviewLayer?.videoGravity = AVLayerVideoGravity.resizeAspectFill
    videoPreviewLayer?.frame = view.layer.bounds
    view.layer.addSublayer(videoPreviewLayer!)
    
    captureSession.startRunning()
    
    view.bringSubview(toFront: messageLabel)
    view.bringSubview(toFront: topbar)
    
    qrCodeFrameView = UIView()
    
    if let qrCodeFrameView = qrCodeFrameView {
      qrCodeFrameView.layer.borderColor = UIColor.green.cgColor
      qrCodeFrameView.layer.borderWidth = 2
      view.addSubview(qrCodeFrameView)
      view.bringSubview(toFront: qrCodeFrameView)
    }
  }
  
  override func didReceiveMemoryWarning() {
    super.didReceiveMemoryWarning()
  }
  
  // MARK: - Helper methods
  
  func launchApp() {
    if presentedViewController != nil {
      return
    }
    
    let navController =  self.storyboard?.instantiateViewController(withIdentifier: "aboutProduct") as! UINavigationController
    let aboutProductController = navController.viewControllers.first as! AboutProductController
    aboutProductController.productId = decodedData
    present(navController, animated: true, completion: nil)
  }
  
}

extension QRScannerController: AVCaptureMetadataOutputObjectsDelegate {
  
  func metadataOutput(_ output: AVCaptureMetadataOutput, didOutput metadataObjects: [AVMetadataObject], from connection: AVCaptureConnection) {
    if metadataObjects.count == 0 {
      qrCodeFrameView?.frame = CGRect.zero
      messageLabel.text = messageText
      return
    }
    
    let metadataObj = metadataObjects[0] as! AVMetadataMachineReadableCodeObject
    
    if supportedCodeTypes.contains(metadataObj.type) {
      let barCodeObject = videoPreviewLayer?.transformedMetadataObject(for: metadataObj)
      qrCodeFrameView?.frame = barCodeObject!.bounds
      
      if metadataObj.stringValue != nil {
        decodedData = metadataObj.stringValue!
        launchApp()
      }
    }
  }
  
}
