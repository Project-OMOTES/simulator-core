<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" id="fdbbf5ee-6e86-4c82-9926-4b59de482378_with_return_network" description="" esdlVersion="v2207" name="Untitled EnergySystem with return network" version="6">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="c615f17e-c077-48c4-8a78-6ae05f8a908f">
    <carriers xsi:type="esdl:Carriers" id="c27258b1-f4f6-4e09-a77a-ce466dbd82d2">
      <carrier xsi:type="esdl:HeatCommodity" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" supplyTemperature="80.0" name="HeatSupply"/>
      <carrier xsi:type="esdl:HeatCommodity" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" returnTemperature="40.0" name="HeatReturn"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="f61a1799-bf04-416a-b15e-93097722ada7">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" multiplier="MEGA" unit="WATT" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" multiplier="KILO" unit="WATTHOUR" id="12c481c0-f81e-49b6-9767-90457684d24a" description="Energy in kWh"/>
    </quantityAndUnits>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="a357cbbe-f277-42b1-8456-cbbadc8ceb2e" name="Untitled Instance">
    <area xsi:type="esdl:Area" id="e4002c22-abd5-43f6-81a8-e6b5f960bfa5" name="Untitled Area">
      <asset xsi:type="esdl:HeatingDemand" name="HeatingDemand_48f3" id="48f3e425-2143-4dcd-9101-c7e22559e82b">
        <port xsi:type="esdl:InPort" id="af0904f7-ba1f-4e79-9040-71e08041601b" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In" connectedTo="3f2dc09a-0cee-44bd-a337-cea55461a334"/>
        <port xsi:type="esdl:OutPort" id="e890f65f-80e7-46fa-8c52-5385324bf686" connectedTo="422cb921-23d2-4410-9072-aaa5796a0620" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out">
          <profile xsi:type="esdl:InfluxDBProfile" field="demand4_MW" database="energy_profiles" measurement="WarmingUp default profiles" id="b77e41bc-a5ca-4823-b467-09872f2b6772" startDate="2018-12-31T23:00:00.000000+0000" filters="" host="profiles.warmingup.info" port="443" endDate="2019-12-31T22:00:00.000000+0000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <geometry xsi:type="esdl:Point" lat="52.158769628869045" lon="4.63726043701172" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" name="Expensive_source" id="cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4" power="5000000.0">
        <costInformation xsi:type="esdl:CostInformation" id="c547cd7d-1851-41ae-b6a9-989f6f280a22">
          <marginalCosts xsi:type="esdl:SingleValue" id="b14b4e00-d596-452d-9795-1fc729ad7147" value="0.5">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perMultiplier="KILO" physicalQuantity="COST" perUnit="WATT" unit="EURO" id="991a5069-5396-4977-ab05-3e7e5a866dba" description="Cost in EUR/kW"/>
          </marginalCosts>
        </costInformation>
        <port xsi:type="esdl:OutPort" id="2d818e3d-8a39-4cec-afa0-f6dbbfd50696" connectedTo="a9793a5e-df4f-4795-8079-015dfaf57f82" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <port xsi:type="esdl:InPort" id="9c258b9d-3149-4720-8931-f4bef1080ec1" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In" connectedTo="935fb733-9f76-4a8d-8899-1ad8689a4b12"/>
        <geometry xsi:type="esdl:Point" lat="52.148869383489114" lon="4.558639526367188" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe1_a" innerDiameter="0.1" length="2540.54" id="8a865bea-a043-481d-a7c9-ea26e1b91d8e" related="">
        <port xsi:type="esdl:InPort" id="a9793a5e-df4f-4795-8079-015dfaf57f82" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In" connectedTo="2d818e3d-8a39-4cec-afa0-f6dbbfd50696"/>
        <port xsi:type="esdl:OutPort" id="1419d0fb-f2d3-4772-ae53-698e46c3196b" connectedTo="395aed29-7d11-4bbb-a637-6bd33caf14e4" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.148869383489114" lon="4.558639526367188"/>
          <point xsi:type="esdl:Point" lat="52.16354781580642" lon="4.587178230285645"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe1_b" innerDiameter="0.1" length="3726.43" id="b85e992d-1d31-4708-bb43-3df55b5b8627" related="">
        <port xsi:type="esdl:InPort" id="28c5d2f2-c5f7-4b43-97a3-42acc609c43f" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In" connectedTo="3d96041c-5c28-43c2-ac08-5719c1d977d3"/>
        <port xsi:type="esdl:OutPort" id="3f2dc09a-0cee-44bd-a337-cea55461a334" connectedTo="af0904f7-ba1f-4e79-9040-71e08041601b" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.16354781580642" lon="4.587178230285645"/>
          <point xsi:type="esdl:Point" lat="52.16740421514521" lon="4.594688415527345"/>
          <point xsi:type="esdl:Point" lat="52.158769628869045" lon="4.63726043701172"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_6930" id="69308f2b-d327-471f-a3ee-0d50d68e3b30">
        <port xsi:type="esdl:InPort" id="395aed29-7d11-4bbb-a637-6bd33caf14e4" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In" connectedTo="1419d0fb-f2d3-4772-ae53-698e46c3196b 89c6f182-d35f-4812-ad1b-72e4e575ff75"/>
        <port xsi:type="esdl:OutPort" id="3d96041c-5c28-43c2-ac08-5719c1d977d3" connectedTo="28c5d2f2-c5f7-4b43-97a3-42acc609c43f" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <geometry xsi:type="esdl:Point" lat="52.16354781580642" lon="4.587178230285645"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe1_ret_a" innerDiameter="0.1" length="3717.24" id="1b929c8e-d7c2-4c98-bdb2-f64fdb8ab0cd" related="">
        <port xsi:type="esdl:InPort" id="422cb921-23d2-4410-9072-aaa5796a0620" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In_ret" connectedTo="e890f65f-80e7-46fa-8c52-5385324bf686"/>
        <port xsi:type="esdl:OutPort" id="1b2d956a-db2c-44fd-b8d6-00bdc58f2bb1" connectedTo="58053eb8-fa90-4166-891b-ed918459a72b" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.15885962895904" lon="4.636858896813017"/>
          <point xsi:type="esdl:Point" lat="52.16749421523521" lon="4.5942969754153795" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lat="52.16368272961575" lon="4.586888551712037"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe1_ret_b" innerDiameter="0.1" length="2550.24" id="c091c427-5ce4-45af-a51d-d614bce4a620" related="">
        <port xsi:type="esdl:InPort" id="2e5bbf02-4a0a-443b-bb4c-a5daf7d8f97b" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In" connectedTo="c1b24bfb-073a-428c-99c7-6bc8adb0476a"/>
        <port xsi:type="esdl:OutPort" id="935fb733-9f76-4a8d-8899-1ad8689a4b12" connectedTo="9c258b9d-3149-4720-8931-f4bef1080ec1" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out_ret"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.16368272961575" lon="4.586888551712037"/>
          <point xsi:type="esdl:Point" lat="52.14895938357911" lon="4.558225705568235" CRS="WGS84"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_1bb6" id="1bb619ab-30c7-4016-abab-3ffe49a18cf4">
        <port xsi:type="esdl:InPort" id="58053eb8-fa90-4166-891b-ed918459a72b" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In" connectedTo="1b2d956a-db2c-44fd-b8d6-00bdc58f2bb1"/>
        <port xsi:type="esdl:OutPort" id="c1b24bfb-073a-428c-99c7-6bc8adb0476a" connectedTo="2e5bbf02-4a0a-443b-bb4c-a5daf7d8f97b 1664ff39-bbd6-4e87-9757-c8594eba1f68" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out"/>
        <geometry xsi:type="esdl:Point" lat="52.16368272961575" lon="4.586888551712037"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" name="Cheap_source" id="485462dc-60b2-4a9f-94c9-4d17af21e2d8" power="1000000.0">
        <costInformation xsi:type="esdl:CostInformation" id="c160435b-e35b-470f-8a25-e0b45ff97f4b">
          <marginalCosts xsi:type="esdl:SingleValue" id="aecc006e-f1ea-4f3f-b63d-2792261d0720" value="0.32">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perMultiplier="KILO" physicalQuantity="COST" perUnit="WATTHOUR" unit="EURO" id="8338c0cd-c2ef-4a34-a8eb-0fd9473232c9" description="Cost in EUR/kWh"/>
          </marginalCosts>
        </costInformation>
		<port xsi:type="esdl:InPort" id="5cdab611-1d3f-4273-9272-ed4a234e1098" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In" connectedTo="469b8bbd-1eff-4ef6-abb8-5798a0732445"/>
        <port xsi:type="esdl:OutPort" id="15f05e3f-75b8-40a5-a65e-d08f7148b991" connectedTo="dcdaa42e-ebde-412d-8fd4-b1fd189b92d4" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <geometry xsi:type="esdl:Point" lat="52.162988412720885" lon="4.587698578834535" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe_624b" length="71.6" id="624be2a2-b0ea-4732-9490-4523fd7b73b4" innerDiameter="0.1">
        <port xsi:type="esdl:InPort" id="dcdaa42e-ebde-412d-8fd4-b1fd189b92d4" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In" connectedTo="15f05e3f-75b8-40a5-a65e-d08f7148b991"/>
        <port xsi:type="esdl:OutPort" id="89c6f182-d35f-4812-ad1b-72e4e575ff75" connectedTo="395aed29-7d11-4bbb-a637-6bd33caf14e4" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.162988412720885" lon="4.587698578834535"/>
          <point xsi:type="esdl:Point" lat="52.16354781580642" lon="4.587178230285645"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe_0b3e" length="94.9" id="0b3ea889-1822-4208-9aa0-d6b2b3ca1dd3" innerDiameter="0.1">
        <port xsi:type="esdl:InPort" id="1664ff39-bbd6-4e87-9757-c8594eba1f68" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In" connectedTo="c1b24bfb-073a-428c-99c7-6bc8adb0476a"/>
        <port xsi:type="esdl:OutPort" id="469b8bbd-1eff-4ef6-abb8-5798a0732445" connectedTo="5cdab611-1d3f-4273-9272-ed4a234e1098" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.16368272961575" lon="4.586888551712037"/>
          <point xsi:type="esdl:Point" lat="52.162988412720885" lon="4.587698578834535"/>
        </geometry>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
