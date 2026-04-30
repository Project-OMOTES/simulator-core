<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" id="fdbbf5ee-6e86-4c82-9926-4b59de482378_with_return_network" description="" esdlVersion="v2207" name="Untitled EnergySystem with return network" version="4">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="c615f17e-c077-48c4-8a78-6ae05f8a908f">
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="f61a1799-bf04-416a-b15e-93097722ada7">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" multiplier="MEGA" unit="WATT" description="Power in MW"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" id="12c481c0-f81e-49b6-9767-90457684d24a" multiplier="KILO" unit="WATTHOUR" description="Energy in kWh"/>
    </quantityAndUnits>
    <carriers xsi:type="esdl:Carriers" id="c27258b1-f4f6-4e09-a77a-ce466dbd82d2">
      <carrier xsi:type="esdl:HeatCommodity" supplyTemperature="60.0" name="HeatSupply" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
      <carrier xsi:type="esdl:HeatCommodity" returnTemperature="40.0" name="HeatReturn" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
      <carrier xsi:type="esdl:HeatCommodity" id="34859981-9666-43f0-9ce4-ebf64bf075d7" name="Secondaryheat" supplyTemperature="50.0" returnTemperature="30.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="c24910dd-b95d-4d15-9e30-07503fd99967" name="secondaryheat_2" supplyTemperature="50.0" returnTemperature="30.0"/>
    </carriers>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="a357cbbe-f277-42b1-8456-cbbadc8ceb2e" name="Untitled Instance">
    <area xsi:type="esdl:Area" name="Untitled Area" id="e4002c22-abd5-43f6-81a8-e6b5f960bfa5">
      <asset xsi:type="esdl:HeatingDemand" id="48f3e425-2143-4dcd-9101-c7e22559e82b" name="HeatingDemand_48f3">
        <port xsi:type="esdl:InPort" id="af0904f7-ba1f-4e79-9040-71e08041601b" name="In" connectedTo="3f2dc09a-0cee-44bd-a337-cea55461a334" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
        <port xsi:type="esdl:OutPort" id="e890f65f-80e7-46fa-8c52-5385324bf686" name="Out" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" connectedTo="422cb921-23d2-4410-9072-aaa5796a0620">
          <profile xsi:type="esdl:InfluxDBProfile" endDate="2019-12-31T22:00:00.000000+0000" id="b77e41bc-a5ca-4823-b467-09872f2b6772" port="443" host="profiles.warmingup.info" filters="" startDate="2018-12-31T23:00:00.000000+0000" database="energy_profiles" measurement="WarmingUp default profiles" field="demand4_MW">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lon="4.63726043701172" lat="52.158769628869045"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" power="500000.0" id="cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4" name="GenericProducer_cf3d">
        <port xsi:type="esdl:InPort" id="9c258b9d-3149-4720-8931-f4bef1080ec1" name="In" connectedTo="935fb733-9f76-4a8d-8899-1ad8689a4b12" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <port xsi:type="esdl:OutPort" id="2d818e3d-8a39-4cec-afa0-f6dbbfd50696" name="Out" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" connectedTo="a9793a5e-df4f-4795-8079-015dfaf57f82"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lon="4.558639526367188" lat="52.148869383489114"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="1dd243a2-706c-4c4a-ac82-9cda5f64a662" length="3148.28" name="Pipe1_a" innerDiameter="0.1" related="">
        <port xsi:type="esdl:InPort" id="a9793a5e-df4f-4795-8079-015dfaf57f82" name="In" connectedTo="2d818e3d-8a39-4cec-afa0-f6dbbfd50696" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
        <port xsi:type="esdl:OutPort" id="0eb2ade3-d6d0-45b2-823a-f6301bf803fd" name="Out" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" connectedTo="3c420696-d3b7-40d2-816e-2558c9258739"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.148869383489114" lon="4.558639526367188"/>
          <point xsi:type="esdl:Point" lat="52.16705873224708" lon="4.594007134437562"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" id="924aa32f-5dbe-4bac-b8e0-fb6ce9241518" length="3118.69" name="Pipe1_b" innerDiameter="0.1" related="">
        <port xsi:type="esdl:InPort" id="f805edce-109b-4c8f-96c5-925f56688c08" name="In" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" connectedTo="3c924a68-29dc-46a4-8e9f-135915370276"/>
        <port xsi:type="esdl:OutPort" id="3f2dc09a-0cee-44bd-a337-cea55461a334" name="Out" connectedTo="af0904f7-ba1f-4e79-9040-71e08041601b" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.16705873224708" lon="4.594007134437562"/>
          <point xsi:type="esdl:Point" lon="4.594688415527345" lat="52.16740421514521"/>
          <point xsi:type="esdl:Point" lon="4.63726043701172" lat="52.158769628869045"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Joint" id="e64c67bc-5507-4c07-8f27-e88c971b0a46" name="Joint_e64c">
        <port xsi:type="esdl:InPort" id="3c420696-d3b7-40d2-816e-2558c9258739" name="In" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" connectedTo="0eb2ade3-d6d0-45b2-823a-f6301bf803fd 82b47cf6-b224-4c0b-9840-d98c8cbb7d60"/>
        <port xsi:type="esdl:OutPort" id="3c924a68-29dc-46a4-8e9f-135915370276" name="Out" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" connectedTo="f805edce-109b-4c8f-96c5-925f56688c08"/>
        <geometry xsi:type="esdl:Point" lat="52.16705873224708" lon="4.594007134437562"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="ca9ffbee-f056-4bff-a4eb-e1f232548b1a" length="3112.32" name="Pipe1_ret_a" innerDiameter="0.1" related="">
        <port xsi:type="esdl:InPort" id="422cb921-23d2-4410-9072-aaa5796a0620" name="In_ret" connectedTo="e890f65f-80e7-46fa-8c52-5385324bf686" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <port xsi:type="esdl:OutPort" id="16b6a0c1-305b-4560-b9b0-d6252945a0bc" name="Out" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" connectedTo="7ec99d06-2fdf-4224-a362-5eb489e9307e"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.15885962895904" lon="4.636858896813017"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lon="4.5942969754153795" lat="52.16749421523521"/>
          <point xsi:type="esdl:Point" lat="52.16717389351117" lon="4.593690633773805"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" id="85e69e40-a553-492f-bb9a-cdd0d6a819e2" length="3155.16" name="Pipe1_ret_b" innerDiameter="0.1" related="">
        <port xsi:type="esdl:InPort" id="a7492239-9fbc-42fd-81eb-42df86cc6d68" name="In" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" connectedTo="1ace2635-d4fd-4ff7-b296-9c6711758658"/>
        <port xsi:type="esdl:OutPort" id="935fb733-9f76-4a8d-8899-1ad8689a4b12" name="Out_ret" connectedTo="9c258b9d-3149-4720-8931-f4bef1080ec1" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.16717389351117" lon="4.593690633773805"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lon="4.558225705568235" lat="52.14895938357911"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Joint" id="e518886b-fa13-4ec2-aac6-b0eedefa6d3b" name="Joint_e518">
        <port xsi:type="esdl:InPort" id="7ec99d06-2fdf-4224-a362-5eb489e9307e" name="In" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" connectedTo="16b6a0c1-305b-4560-b9b0-d6252945a0bc"/>
        <port xsi:type="esdl:OutPort" id="1ace2635-d4fd-4ff7-b296-9c6711758658" name="Out" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" connectedTo="a7492239-9fbc-42fd-81eb-42df86cc6d68 ad8ebc5e-6658-471b-8d53-1f2d44352fe4"/>
        <geometry xsi:type="esdl:Point" lat="52.16717389351117" lon="4.593690633773805"/>
      </asset>
      <asset xsi:type="esdl:HeatPump" id="d90ca53c-03cf-4e08-a7a8-a81b5090e7d9" name="HeatPump_d90c" COP="5.0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.166269046978364" lon="4.595074653625489"/>
        <port xsi:type="esdl:InPort" id="55d4ea5c-c3f8-4f19-912b-8b6663405692" name="PrimIn" connectedTo="565430a5-0980-48b5-8c0f-4d33e3d72b69" carrier="c24910dd-b95d-4d15-9e30-07503fd99967"/>
        <port xsi:type="esdl:OutPort" id="1f605804-592c-4958-8d3a-8198ea1f31b5" name="PrimOut" connectedTo="5a1ed3f1-b208-4751-ba2a-e8fc58ff9dd1" carrier="34859981-9666-43f0-9ce4-ebf64bf075d7"/>
        <port xsi:type="esdl:InPort" id="681d0faf-f1c0-44f0-b2f6-7a402ed3e336" name="SecIn" connectedTo="3181a4ee-92db-4a28-be6e-172810f53dee" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <port xsi:type="esdl:OutPort" id="f4a6cc67-a51b-458b-b941-4aa4a32662e8" name="SecOut" connectedTo="b5a6edd6-7631-4feb-a45f-7ae9f8ee7326" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
      </asset>
      <asset xsi:type="esdl:ATES" id="e8a5a89d-d58e-4991-a920-2a573f2b257c" name="ATES_e8a5" maxChargeRate="11610000.0" maxDischargeRate="11610000.0" aquiferTopDepth="300.0" aquiferThickness="45.0" aquiferMidTemperature="17.0" aquiferNetToGross="1.0" aquiferPorosity="0.3" aquiferPermeability="10000.0" aquiferAnisotropy="4.0" salinity="10000.0" wellCasingSize="13.0" wellDistance="150.0">
        <dataSource xsi:type="esdl:DataSource" name="WarmingUp factsheet: HT-ATES (high)" description="This data was generated using the 'kosten_per_asset.xslx' file in the 'Kentallen' directory of WarmingUp project 1D" attribution=""/>
        <costInformation xsi:type="esdl:CostInformation">
          <investmentCosts xsi:type="esdl:SingleValue" value="2333594.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" description="Cost in EUR" id="05da15c0-19dd-478b-8deb-facdca776158"/>
          </investmentCosts>
          <variableOperationalCosts xsi:type="esdl:SingleValue" value="69666.67">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" description="Cost in EUR/yr" perTimeUnit="YEAR" id="c60f06a4-2300-4ce9-ae04-73f4832ddbf2"/>
          </variableOperationalCosts>
          <fixedMaintenanceCosts xsi:type="esdl:SingleValue" value="115472.22">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" description="Cost in EUR/yr" perTimeUnit="YEAR" id="cdabd29a-45a7-4b2d-95f9-c983c1f9d6b2"/>
          </fixedMaintenanceCosts>
          <fixedOperationalCosts xsi:type="esdl:SingleValue" value="30000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" description="Cost in EUR/yr" perTimeUnit="YEAR" id="611747a6-c9fb-4653-9e93-eb4d41583700"/>
          </fixedOperationalCosts>
        </costInformation>
        <geometry xsi:type="esdl:Point" lat="52.16591861965104" lon="4.594599902629853" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="fc60bd79-f073-48c9-8f55-d9c5e9f8ad53" name="In" connectedTo="9e29818b-5d80-448f-8775-96d126af3ca7" carrier="34859981-9666-43f0-9ce4-ebf64bf075d7"/>
        <port xsi:type="esdl:OutPort" id="e5ace3c3-79e5-4d3f-be60-e2614933db40" name="Out" connectedTo="1b7e9a24-c888-4400-ba91-5db03fb73b1c" carrier="c24910dd-b95d-4d15-9e30-07503fd99967"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="647c53e3-6e5c-49e4-8868-6c06e31afb84" name="Pipe_647c" innerDiameter="0.1603" outerDiameter="0.25" diameter="DN150" length="54.8">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="7887012f-9817-4d61-96e5-8599088c19a9">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="034f0581-0750-4854-8ef9-26e660656862" value="1126.4">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="b86415ee-0dd1-427d-9ebc-f1b1bfdda2a7"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.004">
            <matter xsi:type="esdl:Material" name="steel" id="46684f23-7025-4f16-9c77-8b091cf1758e" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.03725">
            <matter xsi:type="esdl:Material" name="PUR" id="62d6c9ec-135f-4cc1-8569-a5cbaabde304" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0036">
            <matter xsi:type="esdl:Material" name="HDPE" id="79c5a4b6-530e-4692-bbdb-1b6941e38369" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.16591861965104" lon="4.594599902629853"/>
          <point xsi:type="esdl:Point" lat="52.16594000731348" lon="4.59479570388794"/>
          <point xsi:type="esdl:Point" lat="52.166269046978364" lon="4.595074653625489"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="1b7e9a24-c888-4400-ba91-5db03fb73b1c" name="In" connectedTo="e5ace3c3-79e5-4d3f-be60-e2614933db40" carrier="c24910dd-b95d-4d15-9e30-07503fd99967"/>
        <port xsi:type="esdl:OutPort" id="565430a5-0980-48b5-8c0f-4d33e3d72b69" name="Out" connectedTo="55d4ea5c-c3f8-4f19-912b-8b6663405692" carrier="c24910dd-b95d-4d15-9e30-07503fd99967"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="2252e205-a602-4343-b198-00ed3df693fe" name="Pipe_2252" innerDiameter="0.1603" outerDiameter="0.25" diameter="DN150" length="92.6">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="9cad7bba-1bff-4658-8d40-5c3b1a1b2ad4">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="7dcb9ed9-819d-41c0-acc1-8ca877f50e3e" value="1126.4">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="e6195122-076c-4b44-80fe-225f731095a8"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.004">
            <matter xsi:type="esdl:Material" name="steel" id="b80bb865-f3bc-4ae6-87f7-199442385983" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.03725">
            <matter xsi:type="esdl:Material" name="PUR" id="9d048930-ac88-4694-a7dd-380be57de543" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0036">
            <matter xsi:type="esdl:Material" name="HDPE" id="b2752826-a0a2-4f4e-b49e-eab7dffa271b" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.166269046978364" lon="4.595074653625489"/>
          <point xsi:type="esdl:Point" lat="52.16633320942954" lon="4.594556987285615"/>
          <point xsi:type="esdl:Point" lat="52.16601733185342" lon="4.594369232654572"/>
          <point xsi:type="esdl:Point" lat="52.16591861965104" lon="4.594599902629853"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="5a1ed3f1-b208-4751-ba2a-e8fc58ff9dd1" name="In" connectedTo="1f605804-592c-4958-8d3a-8198ea1f31b5" carrier="34859981-9666-43f0-9ce4-ebf64bf075d7"/>
        <port xsi:type="esdl:OutPort" id="9e29818b-5d80-448f-8775-96d126af3ca7" name="Out" connectedTo="fc60bd79-f073-48c9-8f55-d9c5e9f8ad53" carrier="34859981-9666-43f0-9ce4-ebf64bf075d7"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="d990320a-5b7a-42b6-b680-0597d15daa60" name="Pipe_d990" innerDiameter="0.1603" outerDiameter="0.25" diameter="DN150" length="168.8">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="8f1df178-2493-42c1-acaf-d6de186efc1a">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="6d83b3e2-492d-4892-b06a-80af9d5fa602" value="1126.4">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="2a53f1e9-a38d-4362-8185-74208ac83c75"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.004">
            <matter xsi:type="esdl:Material" name="steel" id="ec36f6d9-9ac2-4195-b455-47c9cc30ad41" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.03725">
            <matter xsi:type="esdl:Material" name="PUR" id="8262b8fe-747b-4438-bb7e-d53cbb322d6b" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0036">
            <matter xsi:type="esdl:Material" name="HDPE" id="1325be4c-346e-42d8-8e39-bcdf7c43da41" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.16717389351117" lon="4.593690633773805"/>
          <point xsi:type="esdl:Point" lat="52.166897505976614" lon="4.593915939331056"/>
          <point xsi:type="esdl:Point" lat="52.16690573182086" lon="4.5948171615600595"/>
          <point xsi:type="esdl:Point" lat="52.166269046978364" lon="4.595074653625489"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="ad8ebc5e-6658-471b-8d53-1f2d44352fe4" name="In" connectedTo="1ace2635-d4fd-4ff7-b296-9c6711758658" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <port xsi:type="esdl:OutPort" id="3181a4ee-92db-4a28-be6e-172810f53dee" name="Out" connectedTo="681d0faf-f1c0-44f0-b2f6-7a402ed3e336" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="a87dff89-4d91-4a49-9f24-853cf5f07360" name="Pipe_a87d" innerDiameter="0.1603" outerDiameter="0.25" diameter="DN150" length="147.8">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="0d08ffcb-1838-492b-88c7-61f8ddaff8b7">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="c10ea84f-2896-4647-abd3-ae5085cdee80" value="1126.4">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="e97ffceb-5625-4308-b65d-96de7dec03dc"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.004">
            <matter xsi:type="esdl:Material" name="steel" id="28f23838-69b5-48d7-b988-0cd2bfeb0e3a" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.03725">
            <matter xsi:type="esdl:Material" name="PUR" id="0273986c-8f93-4c5f-a716-060c21bed7db" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0036">
            <matter xsi:type="esdl:Material" name="HDPE" id="782da7e8-ae92-42ac-b81e-a508d7dc6dd0" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.166269046978364" lon="4.595074653625489"/>
          <point xsi:type="esdl:Point" lat="52.16645536460967" lon="4.595167189836503"/>
          <point xsi:type="esdl:Point" lat="52.1666145360079" lon="4.5950424671173105"/>
          <point xsi:type="esdl:Point" lat="52.16701924831649" lon="4.594886898994447"/>
          <point xsi:type="esdl:Point" lat="52.167057087084" lon="4.594304859638215"/>
          <point xsi:type="esdl:Point" lat="52.16705873224708" lon="4.594007134437562"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="b5a6edd6-7631-4feb-a45f-7ae9f8ee7326" name="In" connectedTo="f4a6cc67-a51b-458b-b941-4aa4a32662e8" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
        <port xsi:type="esdl:OutPort" id="82b47cf6-b224-4c0b-9840-d98c8cbb7d60" name="Out" connectedTo="3c420696-d3b7-40d2-816e-2558c9258739" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
