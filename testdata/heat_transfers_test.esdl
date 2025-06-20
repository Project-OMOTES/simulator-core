<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="heat_pump_test with return network" id="0c234aef-e3d6-4a3f-b455-3fba2da8bb55_with_return_network" esdlVersion="v2401" description="" version="6">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="07d4d3c9-36b7-496c-9fce-d90b46e13321">
    <carriers xsi:type="esdl:Carriers" id="6305e67d-de4f-43cc-bfd1-c5eef55f927c">
      <carrier xsi:type="esdl:HeatCommodity" id="10e5076b-f5af-45c7-85c9-f21408004f13" name="hot" supplyTemperature="80.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="af34b568-9478-4501-a7b4-e25587843544" name="cold" supplyTemperature="50.0"/>
      <carrier xsi:type="esdl:HeatCommodity" returnTemperature="40.0" name="hot_ret" id="10e5076b-f5af-45c7-85c9-f21408004f13_ret"/>
      <carrier xsi:type="esdl:HeatCommodity" returnTemperature="30.0" name="cold_ret" id="af34b568-9478-4501-a7b4-e25587843544_ret"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="b97135ab-f45a-4a5e-8f41-cca7a85fea18">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" physicalQuantity="POWER" multiplier="MEGA" unit="WATT"/>
    </quantityAndUnits>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="430d7795-2ad1-46ae-ad7f-c83106246c88" name="Untitled instance">
    <area xsi:type="esdl:Area" id="a523e51b-0e81-427b-82ac-81606421ebc2" name="Untitled area">
      <asset xsi:type="esdl:GenericConsumer" name="GenericConsumer_1b6b" id="1b6b2418-bf1f-4b6c-807e-081f24b9aeb7">
        <geometry xsi:type="esdl:Point" lon="4.4864022731781015" CRS="WGS84" lat="52.05152721851609"/>
        <port xsi:type="esdl:InPort" id="d9e9f2cd-db64-48f3-8924-36ff032b9217" name="In" carrier="10e5076b-f5af-45c7-85c9-f21408004f13" connectedTo="762b7367-4f4f-40b4-aa38-2b35dbfd71f2"/>
        <port xsi:type="esdl:OutPort" id="883eb369-9b09-490f-a492-fffa50567728" name="Out" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret" connectedTo="de84bc35-c477-459b-9928-9b16628a2989">
          <profile xsi:type="esdl:InfluxDBProfile" multiplier="10.0" measurement="Space Heat default profiles" field="SpaceHeat&amp;HotWater_PowerProfile_1700_1950" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="dc72dbbe-680a-4b8e-b75f-3f04037efc00">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:GenericProducer" name="GenericProducer_1a0a" id="1a0a39f0-91e1-4bcc-a268-fe4480c123e1" power="5000000.0">
        <geometry xsi:type="esdl:Point" lon="4.482411146163941" CRS="WGS84" lat="52.05148763214781"/>
        <port xsi:type="esdl:OutPort" id="225009d9-a56d-4716-9043-10904e9c5e7a" name="Out" carrier="af34b568-9478-4501-a7b4-e25587843544" connectedTo="72bf35ac-e43b-48c1-9746-95464dba9cff"/>
        <port xsi:type="esdl:InPort" id="c4e01a1c-58da-41f9-8c5f-fb1b8d95645e" name="In" carrier="af34b568-9478-4501-a7b4-e25587843544_ret" connectedTo="f5156898-c755-4ea1-ab3b-3bad41afa31e"/>
      </asset>
      <asset xsi:type="esdl:Pipe" innerDiameter="0.1603" name="Pipe2" id="Pipe2" diameter="DN150" length="126.9" outerDiameter="0.315" related="Pipe2_ret">
        <costInformation xsi:type="esdl:CostInformation" id="2c88ec97-b9af-4994-b33e-91530e5bb3ab">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="163b9181-b3e8-4ca5-b950-ef954213b211" value="1126.4">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="METRE" physicalQuantity="COST" unit="EURO" id="a386f328-d397-4dd3-a6bb-0dc4ae1f407f" description="Costs in EUR/m"/>
          </investmentCosts>
        </costInformation>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.05148763214781" lon="4.482411146163941"/>
          <point xsi:type="esdl:Point" lat="52.051504126472196" lon="4.484267234802247"/>
        </geometry>
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <port xsi:type="esdl:InPort" id="72bf35ac-e43b-48c1-9746-95464dba9cff" name="In" connectedTo="225009d9-a56d-4716-9043-10904e9c5e7a" carrier="af34b568-9478-4501-a7b4-e25587843544"/>
        <port xsi:type="esdl:OutPort" id="699dd82d-f226-4939-9eed-fdf6cb01ebaa" name="Out" connectedTo="3975e50c-1bc1-4ed2-b84b-c3840ce92020" carrier="af34b568-9478-4501-a7b4-e25587843544"/>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.004">
            <matter xsi:type="esdl:Material" id="c4b6ff8b-e5fd-4fc4-b4ba-1ae06af25b30" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.06925">
            <matter xsi:type="esdl:Material" id="6042c452-901d-4e3a-8d44-3bc5caf7c7c1" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0041">
            <matter xsi:type="esdl:Material" id="70ec6f85-c62a-42d8-bc49-0891c9d9e645" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe2_ret" diameter="DN150" length="160.6" innerDiameter="0.1603" name="Pipe2_ret" outerDiameter="0.315" related="Pipe2">
        <port xsi:type="esdl:InPort" id="f119099b-6042-4522-9292-86209978b114" name="In_ret" connectedTo="fc094f63-de5c-44aa-b993-39281a9f5e46" carrier="af34b568-9478-4501-a7b4-e25587843544_ret"/>
        <port xsi:type="esdl:OutPort" id="f5156898-c755-4ea1-ab3b-3bad41afa31e" name="Out_ret" connectedTo="c4e01a1c-58da-41f9-8c5f-fb1b8d95645e" carrier="af34b568-9478-4501-a7b4-e25587843544_ret"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.05166082225012" lon="4.484159946441651"/>
          <point xsi:type="esdl:Point" lat="52.05157763223781" lon="4.481815223638314"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" innerDiameter="0.1603" name="Pipe1_a" id="ad405193-5618-4490-9058-dad884f1e834" diameter="DN150" length="43.31" outerDiameter="0.315">
        <costInformation xsi:type="esdl:CostInformation" id="824c248b-b39c-4a33-8fee-2554d2f1ab12">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="163b9181-b3e8-4ca5-b950-ef954213b211" value="1126.4">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="METRE" physicalQuantity="COST" unit="EURO" id="a386f328-d397-4dd3-a6bb-0dc4ae1f407f" description="Costs in EUR/m"/>
          </investmentCosts>
        </costInformation>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.051497528743184" lon="4.484835863113404"/>
          <point xsi:type="esdl:Point" lat="52.05151072420023" lon="4.485468864440919"/>
        </geometry>
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <port xsi:type="esdl:InPort" id="71ce0bf1-7d5f-49e3-8fa4-87737dcbc249" name="In" connectedTo="52908004-5802-49db-9d2a-46a039c88741" carrier="10e5076b-f5af-45c7-85c9-f21408004f13"/>
        <port xsi:type="esdl:OutPort" id="661a587a-09cf-4ae0-adb6-c41dab0cc235" name="Out" carrier="10e5076b-f5af-45c7-85c9-f21408004f13" connectedTo="a33fdfb5-b27d-4ba8-a3e8-3a81d8fdaeb4"/>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.004">
            <matter xsi:type="esdl:Material" id="c4b6ff8b-e5fd-4fc4-b4ba-1ae06af25b30" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.06925">
            <matter xsi:type="esdl:Material" id="6042c452-901d-4e3a-8d44-3bc5caf7c7c1" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0041">
            <matter xsi:type="esdl:Material" id="70ec6f85-c62a-42d8-bc49-0891c9d9e645" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" innerDiameter="0.1603" name="Pipe1_b" id="76e6029f-2160-49f9-bed0-835c6fb27302" diameter="DN150" length="63.85" outerDiameter="0.315">
        <costInformation xsi:type="esdl:CostInformation" id="824c248b-b39c-4a33-8fee-2554d2f1ab12">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="163b9181-b3e8-4ca5-b950-ef954213b211" value="1126.4">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="METRE" physicalQuantity="COST" unit="EURO" id="a386f328-d397-4dd3-a6bb-0dc4ae1f407f" description="Costs in EUR/m"/>
          </investmentCosts>
        </costInformation>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.05151072420023" lon="4.485468864440919"/>
          <point xsi:type="esdl:Point" lat="52.05152721851609" lon="4.4864022731781015"/>
        </geometry>
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <port xsi:type="esdl:InPort" id="1ea6a3e6-b5c3-4dff-8cd5-024a1a1fde6c" name="In" carrier="10e5076b-f5af-45c7-85c9-f21408004f13" connectedTo="6aa61d4b-e736-4919-8ca4-d2d651e1b650"/>
        <port xsi:type="esdl:OutPort" id="762b7367-4f4f-40b4-aa38-2b35dbfd71f2" name="Out" connectedTo="d9e9f2cd-db64-48f3-8924-36ff032b9217" carrier="10e5076b-f5af-45c7-85c9-f21408004f13"/>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.004">
            <matter xsi:type="esdl:Material" id="c4b6ff8b-e5fd-4fc4-b4ba-1ae06af25b30" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.06925">
            <matter xsi:type="esdl:Material" id="6042c452-901d-4e3a-8d44-3bc5caf7c7c1" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0041">
            <matter xsi:type="esdl:Material" id="70ec6f85-c62a-42d8-bc49-0891c9d9e645" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Joint" id="446745e8-6df8-4db6-99ef-5ecab2950264" name="Joint_4467">
        <port xsi:type="esdl:InPort" id="a33fdfb5-b27d-4ba8-a3e8-3a81d8fdaeb4" name="In" connectedTo="661a587a-09cf-4ae0-adb6-c41dab0cc235" carrier="10e5076b-f5af-45c7-85c9-f21408004f13"/>
        <port xsi:type="esdl:OutPort" id="6aa61d4b-e736-4919-8ca4-d2d651e1b650" name="Out" connectedTo="1ea6a3e6-b5c3-4dff-8cd5-024a1a1fde6c 734c675e-ed56-43bf-9ac0-bb8a0cac76d0" carrier="10e5076b-f5af-45c7-85c9-f21408004f13"/>
        <geometry xsi:type="esdl:Point" lat="52.05151072420023" lon="4.485468864440919"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="dfce920d-092d-442a-a6cd-f59a9c1f3c4f" diameter="DN150" length="30.99" innerDiameter="0.1603" name="Pipe1_ret_a" outerDiameter="0.315">
        <port xsi:type="esdl:InPort" id="de84bc35-c477-459b-9928-9b16628a2989" name="In_ret" connectedTo="883eb369-9b09-490f-a492-fffa50567728" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret"/>
        <port xsi:type="esdl:OutPort" id="eb04b9fb-c7bf-496f-bd1a-ab5bb5fc155e" name="Out" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret" connectedTo="bcf8628c-9ce3-46da-8707-674f2631d6f3"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.05161721860609" lon="4.485806458551282"/>
          <point xsi:type="esdl:Point" lat="52.05164927626418" lon="4.485356211662293"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" id="62ef5ecb-fd69-4803-b390-db3a529755bb" diameter="DN150" length="37.77" innerDiameter="0.1603" name="Pipe1_ret_b" outerDiameter="0.315">
        <port xsi:type="esdl:InPort" id="5aaf839a-38c1-4330-b081-9194e05b3161" name="In" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret" connectedTo="48fe90e5-ccfd-4448-905b-614885b7957e"/>
        <port xsi:type="esdl:OutPort" id="b10a1050-ae9e-4d4b-9e6f-f1e4f29d67e7" name="Out_ret" connectedTo="5e8b80ee-8263-446a-ba83-ae6a00d28658" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.05164927626418" lon="4.485356211662293"/>
          <point xsi:type="esdl:Point" lat="52.05169546019003" lon="4.484809041023255"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Joint" id="bc6f8a69-6709-49d2-9220-2f27d3600909" name="Joint_bc6f">
        <port xsi:type="esdl:InPort" id="bcf8628c-9ce3-46da-8707-674f2631d6f3" name="In" connectedTo="eb04b9fb-c7bf-496f-bd1a-ab5bb5fc155e a2272410-a151-4309-92b3-b4e76c16866b" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret"/>
        <port xsi:type="esdl:OutPort" id="48fe90e5-ccfd-4448-905b-614885b7957e" name="Out" connectedTo="5aaf839a-38c1-4330-b081-9194e05b3161" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret"/>
        <geometry xsi:type="esdl:Point" lat="52.05164927626418" lon="4.485356211662293"/>
      </asset>
      <asset xsi:type="esdl:HeatExchange" id="8178f616-c087-4442-ad39-3b5f2201c438" name="HeatExchange_8178">
        <geometry xsi:type="esdl:Point" lat="52.051283102019624" lon="4.485471546649934"/>
        <port xsi:type="esdl:InPort" id="eba18ad6-2502-4c97-bd82-a1f0202015d7" name="PrimIn" connectedTo="992c2d55-d009-482a-ad19-4f2671b987ea" carrier="10e5076b-f5af-45c7-85c9-f21408004f13"/>
        <port xsi:type="esdl:OutPort" id="2c9f115c-6700-449b-a855-0a2aacbb2bf0" name="PrimOut" connectedTo="7472ac4c-ee9e-47b3-9e5f-8f546cfa8d21" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret"/>
        <port xsi:type="esdl:OutPort" id="51331161-87a7-4555-a996-d3ca434cfd43" name="SecOut" connectedTo="623541bb-a733-4217-8449-1c208c7e55eb" carrier="af34b568-9478-4501-a7b4-e25587843544_ret"/>
        <port xsi:type="esdl:InPort" id="79be9054-0099-4d6b-a933-f8e4f9c5898d" name="SecIn" connectedTo="a8b0bf50-f870-4646-b915-a27b7d925f4c" carrier="af34b568-9478-4501-a7b4-e25587843544"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="6edad176-4bef-44c3-a04f-5e874ad57733" name="HeatingDemand_6eda">
        <geometry xsi:type="esdl:Point" lat="52.05115774438151" lon="4.486053586006165"/>
        <port xsi:type="esdl:InPort" id="58f6605a-4ade-4be0-b37f-3e679ca173a5" name="In" connectedTo="54ae2ee3-8733-4202-a21a-1161c8ac024f" carrier="af34b568-9478-4501-a7b4-e25587843544_ret">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="Space Heat default profiles" multiplier="10.0" field="SpaceHeat&amp;HotWater_PowerProfile_1700_1950" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="77c2d33c-2e40-4756-a2d0-42258aad813a">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="98527751-4f18-441d-b645-5ffac1d1c19a" name="Out" connectedTo="a9c6334d-dcab-4f8b-9ee6-2144cb87309e" carrier="af34b568-9478-4501-a7b4-e25587843544"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="3113a0a4-729e-4912-b937-d094992040e0" name="Pipe_3113" innerDiameter="0.263" outerDiameter="0.4" diameter="DN250" length="24.0">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="e6c0bd46-4462-4d85-9de2-9e6218e35dee">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="8dad1cd1-95ff-4c6e-b644-a1d38cfe4b1f" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="eca952d5-fbd9-4efd-a72c-2eb773445f25"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" name="steel" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" name="PUR" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" name="HDPE" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.05151072420023" lon="4.485468864440919"/>
          <point xsi:type="esdl:Point" lat="52.05129794697979" lon="4.485530555248261"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="734c675e-ed56-43bf-9ac0-bb8a0cac76d0" name="In" connectedTo="6aa61d4b-e736-4919-8ca4-d2d651e1b650" carrier="10e5076b-f5af-45c7-85c9-f21408004f13"/>
        <port xsi:type="esdl:OutPort" id="992c2d55-d009-482a-ad19-4f2671b987ea" name="Out" connectedTo="eba18ad6-2502-4c97-bd82-a1f0202015d7" carrier="10e5076b-f5af-45c7-85c9-f21408004f13"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="a4f778db-7989-49fa-b47e-17e793ea1ebc" name="Pipe_a4f7" innerDiameter="0.263" outerDiameter="0.4" diameter="DN250" length="40.8">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="a11c454d-0a75-4109-a586-9fd81eee0f45">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="8dad1cd1-95ff-4c6e-b644-a1d38cfe4b1f" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="eca952d5-fbd9-4efd-a72c-2eb773445f25"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" name="steel" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" name="PUR" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" name="HDPE" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.05129794697979" lon="4.485530555248261"/>
          <point xsi:type="esdl:Point" lat="52.05164927626418" lon="4.485356211662293"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="7472ac4c-ee9e-47b3-9e5f-8f546cfa8d21" name="In" connectedTo="2c9f115c-6700-449b-a855-0a2aacbb2bf0" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret"/>
        <port xsi:type="esdl:OutPort" id="a2272410-a151-4309-92b3-b4e76c16866b" name="Out" connectedTo="bcf8628c-9ce3-46da-8707-674f2631d6f3" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="44f0884f-d981-4c91-be5c-2c3d63977ad0" name="Pipe_44f0" innerDiameter="0.263" outerDiameter="0.4" diameter="DN250" length="28.6">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="751aae48-29c5-4ee4-bbb1-c76f4f1d707a">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="8dad1cd1-95ff-4c6e-b644-a1d38cfe4b1f" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="eca952d5-fbd9-4efd-a72c-2eb773445f25"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" name="steel" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" name="PUR" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" name="HDPE" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.05119238271141" lon="4.485511779785157"/>
          <point xsi:type="esdl:Point" lat="52.05106867426703" lon="4.485879242420197"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="623541bb-a733-4217-8449-1c208c7e55eb" name="In" connectedTo="51331161-87a7-4555-a996-d3ca434cfd43" carrier="af34b568-9478-4501-a7b4-e25587843544_ret"/>
        <port xsi:type="esdl:OutPort" id="54ae2ee3-8733-4202-a21a-1161c8ac024f" name="Out" connectedTo="58f6605a-4ade-4be0-b37f-3e679ca173a5" carrier="af34b568-9478-4501-a7b4-e25587843544_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="aef40395-1a7f-4574-9d36-53a5399af797" name="Pipe_aef4" innerDiameter="0.263" outerDiameter="0.4" diameter="DN250" length="26.3">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="24507401-85d7-4afd-b13b-58eba824ffa2">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="8dad1cd1-95ff-4c6e-b644-a1d38cfe4b1f" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="eca952d5-fbd9-4efd-a72c-2eb773445f25"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" name="steel" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" name="PUR" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" name="HDPE" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.05120062992886" lon="4.48594629764557"/>
          <point xsi:type="esdl:Point" lat="52.05131938969132" lon="4.485613703727723"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="a9c6334d-dcab-4f8b-9ee6-2144cb87309e" name="In" connectedTo="98527751-4f18-441d-b645-5ffac1d1c19a" carrier="af34b568-9478-4501-a7b4-e25587843544"/>
        <port xsi:type="esdl:OutPort" id="a8b0bf50-f870-4646-b915-a27b7d925f4c" name="Out" connectedTo="79be9054-0099-4d6b-a933-f8e4f9c5898d" carrier="af34b568-9478-4501-a7b4-e25587843544"/>
      </asset>
      <asset xsi:type="esdl:HeatPump" id="4986c63c-0e58-48a2-844d-fddd235e110a" name="HeatPump_4986" COP="5.0">
        <geometry xsi:type="esdl:Point" lat="52.05161051471814" lon="4.484561607241631" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="3975e50c-1bc1-4ed2-b84b-c3840ce92020" name="PrimIn" connectedTo="699dd82d-f226-4939-9eed-fdf6cb01ebaa" carrier="af34b568-9478-4501-a7b4-e25587843544"/>
        <port xsi:type="esdl:OutPort" id="fc094f63-de5c-44aa-b993-39281a9f5e46" name="PrimOut" connectedTo="f119099b-6042-4522-9292-86209978b114" carrier="af34b568-9478-4501-a7b4-e25587843544_ret"/>
        <port xsi:type="esdl:InPort" id="5e8b80ee-8263-446a-ba83-ae6a00d28658" name="SecIn" connectedTo="b10a1050-ae9e-4d4b-9e6f-f1e4f29d67e7" carrier="10e5076b-f5af-45c7-85c9-f21408004f13_ret"/>
        <port xsi:type="esdl:OutPort" id="52908004-5802-49db-9d2a-46a039c88741" name="SecOut" connectedTo="71ce0bf1-7d5f-49e3-8fa4-87737dcbc249" carrier="10e5076b-f5af-45c7-85c9-f21408004f13"/>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
