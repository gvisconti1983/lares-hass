# lares-hass

A Home Assistant custom integration for Lares Ksenia 4.0

## Overview

This is a super basic custom component for Lares Ksenia 4.0 integration with Home Assistant.

**Main Issues and Limitations:**

* This is a personal project with no guarantee of functionality or security. Use it with caution at own risk. * **Never use an administrator PIN with this component! Create a dedicated regular user + PIN code!**
* Only two components are supported: Light and Cover. Alarm Panel, Generic Output and Scenarios are not supported at this point.
* For both Light and Cover, only controls are supported, status is not updated at this point.
* For each control, the component initializes a new Websocket connection. Controlling multiple lights or covers simultaneously may break.
* The SSL Websocket implementation has stability issues upon initialization of the Cover component. **If SSL fails at component initialization (normally due to Handshake failure), please restart HASS server** ("Settings" => "Server Controls". Multiple restarts may be necessary).
* The Lares SSL certificate is self signed. For this reason, I disable SSL Certificate authentication, this is vulnerable to man in the middle attacks (The same is true when accessing your Lares Ksenia 4.0 central from your PC/Browser!). **Again: it is highly reccomended that you define a dedicated Lares user + PIN code, dedicated exclusively to HASS, limiting permissions as much as needed**.

## Installation

* Create a folder named "lares-hass" with all the files in this repository under "config/custom-components/".
* Edit configuration.yaml as per the following example:

```
light:
  - platform: lares-hass
    host: wss://XXX.XXX.XXX.XXX/KseniaWsock
    # Replace "XXX.XXX.XXX.XXX" with your Lares Ksenia 4.0 Local Network IP address
    password: YYYYYY
    # Replace "YYYYYY" with your user 6 digit pin
    
cover:
  - platform: lares-hass
    host: wss://XXX.XXX.XXX.XXX/KseniaWsock
    # Replace "XXX.XXX.XXX.XXX" with your Lares Ksenia 4.0 Local Network IP address
    password: YYYYYY
    # Replace "YYYYYY" with your user 6 digit pin. It may be the same user PIN as above.
```










