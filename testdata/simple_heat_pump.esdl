<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" id="1ddb172b-8af1-456f-a802-108fff66f40c" description="" esdlVersion="v2401" name="Untitled EnergySystem" version="1">
  <instance xsi:type="esdl:Instance" id="fb6c06c7-7716-4ba9-ae37-c2640c5e2072" name="Untitled Instance">
    <area xsi:type="esdl:Area" name="Untitled Area" id="ed88aae8-c67d-4946-806b-bd13fe120640">
      <asset xsi:type="esdl:HeatPump" name="HeatPump_80c2" id="HeatPump_80c2">
        <port xsi:type="esdl:InPort" name="PrimIn" id="4612e567-987e-436f-b42a-164e5ac41003" connectedTo="cd75e6a1-d9bc-4c43-88a5-eacc2a3a7c54"/>
        <port xsi:type="esdl:OutPort" name="PrimOut" connectedTo="61860e7e-9e2c-47f3-bfb9-246a2dde0110" id="2b090a14-ed38-4ddc-9c1e-c8086ed99f1a"/>
        <port xsi:type="esdl:InPort" name="SecIn" id="3051c490-1d26-4bea-8af6-bf8821233b06" connectedTo="0cb011f8-8b44-431f-9584-430e46285142"/>
        <port xsi:type="esdl:OutPort" name="SecOut" connectedTo="c4da2e55-e843-41e7-8d9a-d9217873ad2a" id="e11b83fa-c124-46f4-b2dd-41649e0075ab"/>
        <geometry xsi:type="esdl:Point" lat="52.051711954437685" lon="4.483494758605958" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" name="GenericProducer_d46e" id="GenericProducer_d46e">
        <port xsi:type="esdl:OutPort" name="Out" connectedTo="4612e567-987e-436f-b42a-164e5ac41003" id="cd75e6a1-d9bc-4c43-88a5-eacc2a3a7c54"/>
        <port xsi:type="esdl:InPort" name="In" id="61860e7e-9e2c-47f3-bfb9-246a2dde0110" connectedTo="2b090a14-ed38-4ddc-9c1e-c8086ed99f1a"/>
        <geometry xsi:type="esdl:Point" lat="52.05161958657236" lon="4.480876922607423" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:GenericConsumer" name="GenericConsumer_2f32" id="GenericConsumer_2f32">
        <port xsi:type="esdl:InPort" name="In" id="c4da2e55-e843-41e7-8d9a-d9217873ad2a" connectedTo="e11b83fa-c124-46f4-b2dd-41649e0075ab"/>
        <port xsi:type="esdl:OutPort" name="Out" connectedTo="3051c490-1d26-4bea-8af6-bf8821233b06" id="0cb011f8-8b44-431f-9584-430e46285142"/>
        <geometry xsi:type="esdl:Point" lat="52.051672368233085" lon="4.485168457031251" CRS="WGS84"/>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
